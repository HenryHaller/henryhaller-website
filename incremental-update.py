import pprint
import requests, feedparser
import time
import Data
import traceback
import logging

logging.basicConfig(filename='backend.log', level=logging.DEBUG)
logging.info("Running on " + time.strftime("%c"))


for show_title, url, dt, show_id in Data.shows():
	last_updated = time.mktime(dt.timetuple())
	try:
		logging.info(show_title)
		d = requests.get(url).text
		items = feedparser.parse(d)["entries"]
		logging.info("Entries parsed: " + str(len(items)))
		if len(items) == 0: continue
		i = 0
		while time.mktime(items[i]['published_parsed']) > last_updated:
			link = items[i]['links'][1]['href']
			title = items[i]["title"]
			published = items[i]["published"]
			try:
				duration = items[i]["itunes_duration"]
			except:
				duration = None
			Data.insert_episode(show_id, link, title, published, duration)
			i = i + 1
	except:
		print("caught error on ", show_title, title)
		traceback.print_exc()
		exit()

Data.update_timestamps()

logging.info("Shutting Down " + time.strftime("%c"))
logging.info("\___________________________________/")
