import traceback
from datetime import datetime
import time
import db
import urls
import psycopg2
from configparser import ConfigParser
import schema


"""
teardown: drop show and episode tables
init: rebuild basic database
buildup: rebuild the show table from urls.yaml

"""



SQL_SELECT_EPISODE_RECORDS = '''SELECT shows.show_title, episodes.episode_url, episodes.episode_title, insertion_date
		 		FROM episodes
				INNER JOIN shows
				ON episodes.show_id = shows.id
				ORDER BY episode_id DESC
				LIMIT 25'''

def select_episodes():
	conn = None
	rows = None
	episodes = []
	try:
		conn = db.connect()
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
	for row in rows:
		episodes.append(schema.Episode(row))
	return episodes


init_file = "postgres_init.sql"
teardown_file = "postgres_teardown.sql"


def init():
	conn = None
	try:
		conn = db.connect()
		cur = conn.cursor()
		cur.execute(open(init_file, 'r').read())
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
def teardown():
	conn = None
	try:
		conn = db.connect()
		cur = conn.cursor()
		cur.execute(open(teardown_file, 'r').read())
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


SQL_CREATE_SHOW_RECORD = '''INSERT INTO shows(show_title, rss_url) VALUES(%s, %s)'''
def buildup():
	conn = None
	try:
		conn = db.connect()
		cur = conn.cursor()
		for key, value in urls.get_urls().items():
			cur.execute(SQL_CREATE_SHOW_RECORD, (key, value))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


SQL_UPDATE_SHOW_TIMESTAMP = '''UPDATE shows SET ts=now();'''
def update_timestamps():
	conn = None
	try:
		conn = db.connect()
		cur = conn.cursor()
		cur.execute(SQL_UPDATE_SHOW_TIMESTAMP)
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


SQL_SELECT_SHOWS = '''SELECT show_title, rss_url, ts, id FROM shows'''
def shows():
	conn = None
	rows = None
	try:
		conn = db.connect()
		cur = conn.cursor()
		cur.execute(SQL_SELECT_SHOWS)
		rows = cur.fetchall()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	return rows



SQL_INSERT_EPISODE_RECORD = '''INSERT INTO episodes ( episode_url, episode_title, show_id) VALUES (%s, %s, %s) '''
def insert_episode(url, title, id):
	conn = None
	try:
		conn = db.connect()
		cur = conn.cursor()
		cur.execute(SQL_INSERT_EPISODE_RECORD, (url, title, id))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		#traceback.print_exc()
		# likely a duplicate?
	finally:
		if conn is not None:
			conn.close()

SQL_HARVEST_SHOW_TIMESTAMP = '''SELECT ts FROM shows LIMIT 1'''
SQL_MODIFY_SHOWS_TIMESTAMP = '''UPDATE shows SET ts=%s'''
def roll_back_one_day():
	conn = None
	try:
		conn = db.connect()
		cur = conn.cursor()
		cur.execute(SQL_HARVEST_SHOW_TIMESTAMP)
		ts = cur.fetchone()[0]
		ts = time.mktime(ts.timetuple()) # convert to float
		new_time = ts - 60 * 60 * 24
		new_time = time.strftime("%Y-%m-%d %H:%M:%S+00", time.gmtime(new_time))
		cur.execute(SQL_MODIFY_SHOWS_TIMESTAMP, (new_time,))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		traceback.print_exc()
	finally:
		if conn is not None:
			conn.close()
