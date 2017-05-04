Pandas Oracle
===============

This package includes methods for: 

1. Running a specified query, passed in as a string, on an Oracle database and returning the result to a Pandas data frame.

2. Executing a command with no return data.

3. Inserting the contents of a Pandas data frame into an Oracle database table.

----

Installation
------------

::

    pip install pandas_oracle


----

Overview
--------

Sample usage::

    from pandas_oracle.tools as oradf
  
    query1 = "select id, name from students where name like '%Oscar%'"
    query2 = "select class,avg(age) from students group by class"
    ## opening conn
    conn = oradf.open_connection(query,"config.yml")
    ## passing the conn object to the query_to_df 
    df1=query_to_df(query,conn,10000)
    ## passing the conn object to the query_to_df , without to open again
    df2=query_to_df(query2,conn,10)
    ## close connection
    oradf.clone_connection(conn)
      

Returns::
    
              ID                NAME
    0    3298272         Meyer,Oscar
    1    2304928         Wilde,Oscar
    2    7654321        Grouch,Oscar
    .        ...                 ...
    128  2234879    De La Hoya,Oscar
    129  9872322      Peterson,Oscar
    130  9082394       Sanchez,Oscar

    [131 rows x 2 columns]

Sample config file::

    database:
        username: "OGROUCH"
        password: "SECR3TPASSWORD"
        sysdba: "n"
        host: >
                (DESCRIPTION =
                        (ADDRESS = (PROTOCOL = TCP)
                                   (HOST = servername.myschool.edu)
                                   (PORT = 1521)
                        )
                        (CONNECT_DATA = (SERVER = DEDICATED)
                                        (SID = dbname)
                        )
                )

If you don't wish to store your password in the configuration file, you can 
omit that line. If a password isn't present in the configuration file, you 
will be prompted for it at runtime.
You could choose to run as SYSDBA role or not, if the yaml file does not
includes the "sysdba" property, the api will connect like a normal user.
