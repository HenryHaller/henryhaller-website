import Data
import models
import urls

Data.teardown()
Data.init()
for static_show in urls.get_urls():
	print("inserting " + static_show["title"] + " into the database.")
	show = models.Show(static_show["title"], static_show["url"], static_show["color"])
	Data.insert_show(show)
Data.roll_back_one_day()
Data.roll_back_one_day()
Data.roll_back_one_day()
Data.roll_back_one_day()

