import traceback
from datetime import datetime
import time
import db
import urls
import psycopg2
from configparser import ConfigParser
import models


"""
teardown: drop show and episode tables
init: rebuild basic database
buildup: rebuild the show table from urls.yaml

"""

SQL_UPDATE_SHOW_TITLE = '''UPDATE shows SET title = %s WHERE id = %s'''
def update_show_title(title, id):
  conn = None
  try:
    conn = db.connect()
    cur = conn.cursor()
    cur.execute(SQL_UPDATE_SHOW_TITLE, (title, id))
    conn.commit()
    cur.close()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
      conn.close()


SQL_INSERT_USER_RECORD = '''INSERT INTO users (username, passhash, salt) VALUES (%s, %s, %s)'''
def insert_user(username, passhash, salt):
	conn = None
	rows = None
	try:
		conn = db.connect()
		cur = conn.cursor()
		cur.execute(SQL_INSERT_USER_RECORD,  (username, passhash, salt))
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		traceback.print_exc()
	finally:
		if conn is not None:
			conn.close()


SQL_SELECT_USER_RECORD = '''SELECT id, username, passhash, salt FROM users WHERE username = %s LIMIT 1'''
def select_user(username):
	conn = None
	rows = None
	user = None
	try:
		conn = db.connect()
		cur = conn.cursor()
		cur.execute(SQL_SELECT_USER_RECORD, (username, ))
		user = cur.fetchone()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		traceback.print_exc()
	finally:
		if conn is not None:
			conn.close()
	if type(user) == psycopg2.extras.DictRow: user = models.User(user)
	return user



SQL_SELECT_EPISODE_RECORDS = '''SELECT shows.title, episodes.episode_url, episodes.title, insertion_date, duration, shows.small_title, shows.color
		 		FROM episodes
				INNER JOIN shows
				ON episodes.show_id = shows.id
				ORDER BY insertion_date DESC
				LIMIT 8'''

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
		episodes.append(models.Episode(row))
	return episodes


SQL_SELECT_PODVIEW_RECORDS = '''SELECT shows.title, episodes.episode_url, episodes.title, insertion_date, duration, shows.small_title, shows.color
		 		FROM episodes
				INNER JOIN shows
				ON episodes.show_id = shows.id
				WHERE shows.small_title = %s
				ORDER BY insertion_date DESC
				LIMIT 25'''
def select_podview_episodes(small_title):
	conn = None
	rows = None
	episodes = []
	try:
		conn = db.connect()
		cur = conn.cursor()
		cur.execute(SQL_SELECT_PODVIEW_RECORDS, (small_title,))
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
		episodes.append(models.Episode(row))
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
		exit("Error in Init-ing the Database. Stopping.")
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


SQL_CREATE_SHOW_RECORD = '''INSERT INTO shows(title, rss_url, small_title, color) VALUES(%s, %s, %s, %s)'''
def insert_show(show):
	conn = None
	try:
		conn = db.connect()
		cur = conn.cursor()
		cur.execute(SQL_CREATE_SHOW_RECORD, (show.title, show.url, show.small_title, show.color))
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


SQL_SELECT_SHOWS = '''SELECT title, rss_url, ts, id FROM shows'''
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

SQL_INSERT_EPISODE_RECORD_BASE = b'''INSERT INTO episodes ( show_id, episode_url, title, insertion_date, duration) VALUES '''
def insert_episodes(data):
  conn = None
  try:
    conn = db.connect()
    cur = conn.cursor()
    # for row in data:
      # print(cur.mogrify('(%s, %s, %s, %s, %s)', row))
    # print(cur.mogrify('(%s, %s, %s, %s, %s)', row) for row in data)
    text_data = b','.join(cur.mogrify('(%s, %s, %s, %s, %s)', row) for row in data)
    cur.execute(SQL_INSERT_EPISODE_RECORD_BASE + text_data)
    conn.commit()
    cur.close()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    traceback.print_exc()
    # likely a duplicate?
  finally:
    if conn is not None:
      conn.close()

SQL_INSERT_EPISODE_RECORD = '''INSERT INTO episodes ( show_id, episode_url, title, insertion_date, duration) VALUES (%s, %s, %s, %s, %s) '''
def insert_episode(id, url, title, timestamp, duration):
  conn = None
  try:
    conn = db.connect()
    cur = conn.cursor()
    cur.execute(SQL_INSERT_EPISODE_RECORD, (id, url, title, timestamp, duration))
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
