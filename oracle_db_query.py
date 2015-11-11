#! /usr/local/bin python3

import cx_Oracle
import getpass
import yaml
from pandas import DataFrame

def query_to_df(query, config_file):
	with open(config_file, 'r') as ymlfile:
	    cfg = yaml.load(ymlfile)

	user = cfg['database']['username']
	if 'password' in cfg['database']:
		pwd = cfg['database']['password']
	else:
		pwd = getpass.getpass('Database password: ')
	host = cfg['database']['host']

	con = cx_Oracle.connect("{}/{}@{}".format(user, pwd, host))
	cur = con.cursor()
	cur.execute(query)
	r = cur.fetchall()
	cols = [n[0] for n in cur.description]
	cur.close()
	con.close()
	data = DataFrame.from_records(r, columns=cols)
	return(data)
