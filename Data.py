import traceback
from datetime import datetime
import db



SQL_SELECT_EPISODE_RECORDS = '''SELECT shows.show_title, episodes.episode_url, episodes.episode_title
		 		FROM episodes
				INNER JOIN shows
				ON episodes.show_id = shows.id
				ORDER BY episode_id DESC
				LIMIT 25'''
def select_episodes():
	conn = None
	rows = None
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
	return rows

