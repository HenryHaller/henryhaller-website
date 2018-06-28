import hashlib
class Episode():
	show_title = None
	episode_title = None
	url = None
	color = None
	timestamp = None
	duration = None
	small_show_title = None
	def __init__(self, rows):
		self.show_title = rows[0]
		self.url = rows[1]
		self.episode_title = rows[2]
		self.timestamp = rows[3]
		self.duration = rows[4]
		self.small_show_title = rows[5]
		if self.duration == None: self.duration = "No Information."
		h = hashlib.new('sha256')
		h.update(self.episode_title.encode('utf-8'))
		self.color = h.hexdigest()[0:6]


class Show():
	title = None
	url = None
	small_title = None
	def __init__(self, title, url):
		self.title = title
		self.url = url
		self.small_title = self.title.lower().replace(' ', '_')

