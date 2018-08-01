import pprint
import requests, feedparser
import time
import Data
import traceback
import logging

logging.basicConfig(filename='backend.log', level=logging.DEBUG)
logging.info("Running on " + time.strftime("%c"))


for show_title, url, dt, show_id in Data.shows():
  print("Doing full update for " + show_title)
  try:
    logging.info(show_title)
    d = requests.get(url).text
    feed = feedparser.parse(d)
    items = feed["entries"]
    show_title = feed["feed"]["title"]
    Data.update_show_title(show_title, show_id)
    logging.info("Entries parsed: " + str(len(items)))
    if len(items) == 0: continue
    insert_targets = []
    for i in items:
      link = i['links'][1]['href']
      title = i["title"]
      published = i["published"]
      try:
      	duration = i["itunes_duration"]
      except:
        duration = None
      # show_id = str(show_id)
      # print(list(map(lambda x: type(x), [show_id, link, title, published, duration])))
      insert_targets.append([show_id, link, title, published, duration])
    Data.insert_episodes(insert_targets)
  	# Data.insert_episode(show_id, link, title, published, duration)
  except:
    print("caught error on ", show_title, title)
    traceback.print_exc()
    exit()

Data.update_timestamps()

logging.info("Shutting Down " + time.strftime("%c"))
logging.info("\___________________________________/")
