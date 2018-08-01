import Data
import my_session_key
from flask import Flask, send_from_directory, session, redirect, url_for, escape, request
application = Flask(__name__)
import jinja2
from string import ascii_letters, digits
from random import choice
import hashlib
import re

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def valid_url(url): return re.match(regex, url) is not None

application.secret_key = my_session_key.my_session_key
templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)

def salt_password(password):
	salt = ''.join(choice(ascii_letters + digits) for i in range(16))
	salted_password = password + salt
	h = hashlib.new('sha256')
	h.update(salted_password.encode('utf-8'))
	return h.hexdigest(), salt

def check_session(username):
	if 'username' in session: return True
	else: return False

def check_password(username, password):
	user = Data.select_user(username)
	if user != None: return user.test_password(password)
	return False

def check_availability(username):
	return Data.select_user(username) == None

def insert_new_user(username, password):
	passhash, salt = salt_password(password)
	Data.insert_user(username, passhash, salt)


@application.route("/add_rss/", methods=['POST'])
def add_show():
  if 'username' not in sesssion: redirect(url_for("pods_login"))
  feed = request.form["feed"]
  if feed == None: redirect(url_for("pods"))
  if !valid_url(feed): redirect(url_for("pods"))



@application.route("/")
def index():
	TEMPLATE_FILE = "index.jinja2.html"
	template = templateEnv.get_template(TEMPLATE_FILE)
	return template.render()



@application.route("/pods/make_account/", methods=['GET', 'POST'])
def mods_make_account():
	if request.method == 'POST':
		username = request.form["username"]
		password = request.form["password"]
		if check_availability(username):
			insert_new_user(password, username)
			return redirect(url_for("pods_login"))
		else:
			return '''Sorry that username is taken. Please reload the page to try another.'''
	TEMPLATE_FILE = "new_account.jinja2.html"
	template = templateEnv.get_template(TEMPLATE_FILE)
	return template.render()

@application.route("/pods/login/", methods=['GET', 'POST'])
def pods_login():
	if request.method == 'GET':
		if 'username' in session:
			return redirect(url_for("pods"))
		else:
			TEMPLATE_FILE = "login.jinja2.html"
			template = templateEnv.get_template(TEMPLATE_FILE)
			return template.render()
	if request.method == 'POST':
		if check_password(request.form["username"], request.form["password"]):
			session['username'] = request.form['password']
	return redirect(url_for("pods"))

@application.route("/pods/logout/")
def pods_logout():
	session.pop('username', None)
	return redirect(url_for('index'))


@application.route("/pods/")
def pods():
	if 'username' in session:
		TEMPLATE_FILE = "pods_index.jinja2.html"
		template = templateEnv.get_template(TEMPLATE_FILE)
		episodes = Data.select_episodes()
		if episodes == None: return "Episodes = None!"
		return template.render(episodes = episodes)
	else:
		return redirect(url_for("pods_login"))



@application.route('/pods/podview/<string:small_show_title>')
def podview(small_show_title):
	TEMPLATE_FILE = "podview.jinja2.html"
	template = templateEnv.get_template(TEMPLATE_FILE)
	episodes = Data.select_podview_episodes(small_show_title)
	if episodes == None: return "Episodes = None!"
	return template.render(episodes = episodes)


@application.route('/static/<path:path>')
def send_static(path):
	return send_from_directory('js', path)


#if __name__ == "__main__":
#	applicationlication.run(host='0.0.0.0')

