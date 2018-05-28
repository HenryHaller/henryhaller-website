import yaml
def get_urls():
	f = open('urls.yaml', 'r')
	urls = yaml.load(f)
	f.close()
	return urls
