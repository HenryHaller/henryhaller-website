import Data
import schema
import urls

Data.teardown()
Data.init()
for static_show in urls.get_urls():
	show = schema.Show(static_show["title"], static_show["url"], static_show["color"])
	Data.insert_show(show)
Data.roll_back_one_day()
Data.roll_back_one_day()
Data.roll_back_one_day()
Data.roll_back_one_day()

