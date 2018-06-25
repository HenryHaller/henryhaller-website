import pprint
import requests, feedparser
import time
import Data
import traceback
import logging

logging.basicConfig(filename='backend.log', level=logging.DEBUG)
logging.info("Running on " + time.strftime("%c"))


for title, url, dt, id in Data.shows():
	try:
		logging.info(title)
		d = requests.get(url).text
		items = feedparser.parse(d)["entries"]
		logging.info("Entries parsed: " + str(len(items)))
		if len(items) == 0: continue
		i = 0
		while time.mktime(items[i]['published_parsed']) > time.mktime(dt.timetuple()):
			item = items[i]
			logging.info(item["title"])
			published = item["published"]
			try:
				duration = item["itunes_duration"]
			except:
				duration = None
			#print(item["title"], item['links'][1]['href'])
			Data.insert_episode(id, item['links'][1]['href'], item["title"], published, duration)
			i = i + 1
	except:
		print("caught error")
		print(url)
		traceback.print_exc()
		exit()

Data.update_timestamps()

logging.info("Shutting Down " + time.strftime("%c"))
logging.info("\___________________________________/")
