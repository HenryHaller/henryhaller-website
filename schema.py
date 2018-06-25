import hashlib
class Episode():
	show_title = None
	episode_title = None
	url = None
	color = None
	timestamp = None
	duration = None
	def __init__(self, rows):
		self.show_title = rows[0]
		self.url = rows[1]
		self.episode_title = rows[2]
		self.timestamp = rows[3]
		self.duration = rows[4]
		if self.duration == None: self.duration = "No Information."
		h = hashlib.new('sha256')
		h.update(self.show_title.encode('utf-8'))
		self.color = h.hexdigest()[0:6]

