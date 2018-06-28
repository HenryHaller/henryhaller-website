import Data
import schema
import urls

Data.teardown()
Data.init()
for title, url in urls.get_urls().items():
	show = schema.Show(title, url)
	Data.insert_show(show)
Data.roll_back_one_day()
Data.roll_back_one_day()
Data.roll_back_one_day()
Data.roll_back_one_day()

