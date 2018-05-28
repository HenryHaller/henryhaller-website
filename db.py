import os
from configparser import ConfigParser
import psycopg2


if 'DATABASE_URL' in os.environ:
	DATABASE_URL = os.environ['DATABASE_URL']
	def connect():
		return psycopg2.connect(DATABASE_URL, sslmode='require')
else:
	def connect():
		parser = ConfigParser()
		parser.read('database.ini')
		db = {}
		if parser.has_section('postgresql'):
			params = parser.items('postgresql')
			for param in params:
				db[param[0]] = param[1]
		else:
			raise Exception('Section {0} not found in the {1} file'.format('postgresql', 'database.ini'))
		return psycopg2.connect(**db)
