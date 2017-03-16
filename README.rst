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

    pip install oracle_db_tools


----

Overview
--------

Sample usage::

    from pandas_oracle.tools import query_to_df

    query = "select id, name from students where name like '%Oscar%'"
    query_to_df(query, "config.yml")

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