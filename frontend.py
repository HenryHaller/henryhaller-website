import Data
from flask import Flask
application = Flask(__name__)
import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "index.html.jinja2"
template = templateEnv.get_template(TEMPLATE_FILE)



@application.route("/")
def hello():
	episodes = Data.select_episodes()
	return template.render(episodes = episodes)


#if __name__ == "__main__":
#	applicationlication.run(host='0.0.0.0')

