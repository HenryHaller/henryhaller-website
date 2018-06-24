import Data
from flask import Flask, send_from_directory
application = Flask(__name__)
import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "index.html.jinja2"
template = templateEnv.get_template(TEMPLATE_FILE)


@application.route("/")
def hello():
#	shows = []
#	links = []
#	episodes = []
#	i = 2
#	for show, link, episode in Data.select_episodes():
#		shows.append((show, i))
#		links.append((link, i))
#		episodes.append((episode, i))
#		i = i + 1
	episodes = Data.select_episodes()
	if episodes == None: return "Episodes = None!"
	return template.render(episodes = episodes)
#	return template.render(shows = shows,
#				links = links,
#				episodes = episodes)

@application.route('/static/<path:path>')
def send_static(path):
	return send_from_directory('js', path)


#if __name__ == "__main__":
#	applicationlication.run(host='0.0.0.0')

