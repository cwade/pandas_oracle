#! /usr/local/bin python3

import cx_Oracle
import getpass
import yaml
import pandas as pd

def open_connection(config_file: str):
    """Open a new connection to database
       based on yaml file.
       config_file: name of parameter file
    """ 
    ## open configuration file */
    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    ##loading variable username, host
    user = cfg['database']['username']
    host = cfg['database']['host']
    ## verify if sysdba conn or not
    if 'sysdba' in cfg['database']:
            sysdba = cfg['database']['sysdba']
    else:
            sysdba = 'n'
    ## loading password or ask
    if 'password' in cfg['database']:
            pwd = cfg['database']['password']
    else:
            pwd = getpass.getpass('Database password: ')
    if sysdba == 'n':
            return(cx_Oracle.connect("{}/{}@{}".format(user, pwd, host)))
    elif sysdba == 'y':
            return(cx_Oracle.connect("{}/{}@{}".format(user, pwd, host), mode=cx_Oracle.SYSDBA))
    else :
            return(cx_Oracle.connect("{}/{}@{}".format(user, pwd, host)))

def query_to_df(query: str, conn_db: cx_Oracle.Connection, arraysize=10000):
    """Run the query and transform the result to a dataframe
       parameters:
       *) query: str with a query statetement
       *) conn_db: a connection object from cx_oracle or open_connection
       *) arraysize: arrayfetch size
    """ 
    cur = conn_db.cursor()
    ## setting arraysize
    if arraysize :
       cur.arraysize = arraysize
    ## execute query 
    cur.execute(query)
    ## fetch all rows
    r = cur.fetchall()
    cols = [n[0] for n in cur.description]
    cur.close()
    data = pd.DataFrame.from_records(r, columns=cols)
    return(data)

def query_to_df_cc(query: str, config_file: str, arraysize=10000):
    """Run the query and transform the result to a dataframe
       parameters:
       *) query: str with a query statetement
       *) config_file: yaml config file specifying db information
       *) arraysize: arrayfetch size
    """ 
    conn = open_connection(config_file)
    df = query_to_df(query, conn, arraysize)
    close_connection(conn)
    return(df)

def execute(statement: str, conn_db: cx_Oracle.Connection):
    """execute a statement
       parameters:
       *) statement: str with a statetement
       *) conn_db: a connection object from cx_oracle or open_connection
    """
    cur = conn_db.cursor()
    cur.execute(statement)
    conn_db.commit()
    cur.close()

def execute_cc(statement: str, config_file: str):
    """execute a statement
       parameters:
       *) statement: str with a statetement
       *) config_file: yaml config file specifying db information
    """
    conn = open_connection(config_file)
    execute(statement, conn)
    close_connection(conn)
    return()

def insert_multiple(table_name: str, df: pd.DataFrame, conn_db: cx_Oracle.Connection, batch_size=10000):
    """multiple insert
       parameters:
       *) table_name: table_name you're inserting into
       *) df: dataframe being inserted into table
       *) conn_db: a connection object from cx_oracle or open_connection
       *) batch_size: batch size of commit (number of rows)
    """
    cur = conn_db.cursor()
    sql = "INSERT INTO {0} ({1}) VALUES (:{2})".format(table_name,
                                                      ', '.join(df.columns),
                                                      ', :'.join(list(map(str,range(1, len(df.columns)+1)))))

    # Get column types so they can be specified before the insert statement.
    # This avoids an error when inserting dates 
    # See http://cx-oracle.readthedocs.io/en/latest/cursor.html#Cursor.execute
    cur.execute('select * from {} where 1=0'.format(table_name))
    db_types = (d[1] for d in cur.description)
    cur.setinputsizes(*db_types)

    i = 0
    while ((i * batch_size) < len(df)):
        rows = []
        min = i*batch_size
        max = ((i+1)*batch_size)-1
        for x in df.ix[min:max,:].values:
            rows.append([None if pd.isnull(y) else y for y in x])
        cur.executemany(sql, rows)
        conn_db.commit()
        i = i + 1
    cur.close()

def insert_multiple_cc(table_name: str, df: pd.DataFrame, config_file: str, batch_size=10000):
    """multiple insert
       parameters:
       *) table_name: table_name you're inserting into
       *) df: dataframe being inserted into table
       *) config_file: yaml config file specifying db information
       *) batch_size: batch size of commit (number of rows)
    """
    conn = open_connection(config_file)
    insert_multiple(table_name, df, conn, batch_size)
    close_connection(conn)
    return()

def close_connection(conn_db: cx_Oracle.Connection):
    """Close the connection
       parameters:
       *) conn_db : connection object 
    """
    conn_db.close()
