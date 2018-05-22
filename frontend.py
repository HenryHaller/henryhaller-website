import Data
from flask import Flask
app = Flask(__name__)
import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "index.html.jinja2"
template = templateEnv.get_template(TEMPLATE_FILE)



@app.route("/")
def hello():
	episodes = Data.select_episodes()
	return template.render(episodes = episodes)

