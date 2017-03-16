#! /usr/local/bin python3

import cx_Oracle
import getpass
import yaml
from pandas import DataFrame

def open_connection(config_file):
    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    user = cfg['database']['username']
    if 'password' in cfg['database']:
            pwd = cfg['database']['password']
    else:
            pwd = getpass.getpass('Database password: ')
    host = cfg['database']['host']
    return(cx_Oracle.connect("{}/{}@{}".format(user, pwd, host)))

def query_to_df(query, config_file):
    con = open_connection(config_file)
    cur = con.cursor()
    cur.execute(query)
    r = cur.fetchall()
    cols = [n[0] for n in cur.description]
    cur.close()
    con.close()
    data = DataFrame.from_records(r, columns=cols)
    return(data)

def execute(statement, config_file):
    con = open_connection(config_file)
    cur = con.cursor()
    cur.execute(statement)
    con.commit()
    cur.close()
    con.close()

def insert_multiple(table_name, df, config_file, batch_size=5000, print_insert_statements=False):
    con = open_connection(config_file)
    cur = con.cursor()
    sql = "INSERT INTO {0} ({1}) VALUES (:{2})".format(table_name,
                                                      ', '.join(df.columns),
                                                      ', :'.join(list(map(str,range(1, len(df.columns)+1)))))
    i = 0
    while ((i * batch_size) < len(df)):
        rows = []
        min = i*batch_size
        max = ((i+1)*batch_size)-1
        for x in df.ix[min:max,:].values:
            rows.append([None if pd.isnull(y) else y for y in x])
        cur.executemany(sql, rows)
        con.commit()
        i = i + 1
    cur.close()
    con.close()

