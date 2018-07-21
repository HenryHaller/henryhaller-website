import Data
from flask import Flask, send_from_directory
application = Flask(__name__)
import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)


@application.route("/pods/")
def hello():
	TEMPLATE_FILE = "index.html.jinja2"
	template = templateEnv.get_template(TEMPLATE_FILE)
	episodes = Data.select_episodes()
	if episodes == None: return "Episodes = None!"
	return template.render(episodes = episodes)


@application.route('/pods/podview/<string:small_show_title>')
def podview(small_show_title):
	TEMPLATE_FILE = "podview.html.jinja2"
	template = templateEnv.get_template(TEMPLATE_FILE)
	episodes = Data.select_podview_episodes(small_show_title)
	if episodes == None: return "Episodes = None!"
	return template.render(episodes = episodes)


@application.route('/static/<path:path>')
def send_static(path):
	return send_from_directory('js', path)


#if __name__ == "__main__":
#	applicationlication.run(host='0.0.0.0')

