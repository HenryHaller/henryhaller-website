import hashlib
class Episode():
	def __init__(self, rows):
		self.show_title = rows[0]
		self.url = rows[1]
		self.episode_title = rows[2]
		self.timestamp = rows[3]
		self.duration = rows[4]
		self.small_show_title = rows[5]
		self.color = rows[6]
		if self.duration == None: self.duration = "No Information."
		if self.color == None:
			h = hashlib.new('sha256')
			h.update(self.show_title.encode('utf-8'))
			self.color = h.hexdigest()[0:6]


class Show():
	def __init__(self, title, url, color):
		self.title = title
		self.url = url
		self.small_title = self.title.lower().replace(' ', '_')
		self.color = color


class User():
	def __init__(self, atts):
		self.id = atts["id"]
		self.username = atts["username"]
		self.passhash = atts["passhash"]
		self.salt = atts["salt"]
	def test_password(self, password):
		password += self.salt
		h = hashlib.new('sha256')
		h.update(password.encode('utf-8'))
		return h.hexdigest() == self.passhash
