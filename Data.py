import os
import traceback
import psycopg2
from configparser import ConfigParser
from datetime import datetime

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db


DATABASE_URL = os.environ['DATABASE_URL']

SQL_SELECT_EPISODE_RECORDS = '''SELECT shows.show_title, episodes.episode_url, episodes.episode_title
		 		FROM episodes
				INNER JOIN shows
				ON episodes.show_id = shows.id LIMIT 25'''
def select_episodes():
	conn = None
	rows = None
	try:
		params = config()
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cur = conn.cursor()
		cur.execute(SQL_SELECT_EPISODE_RECORDS)
		rows = cur.fetchall()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		traceback.print_exc()
		# likely a duplicate?
	finally:
		if conn is not None:
			conn.close()
	return rows

