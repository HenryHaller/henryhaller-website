import os


if 'SESSION_KEY' in os.environ:
	my_session_key = os.environ['SESSION_KEY']
else:
	import session_key
	my_session_key = session_key.key
