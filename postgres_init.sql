CREATE TABLE shows (
	id SERIAL PRIMARY KEY,
	title TEXT,
	small_title TEXT,
	rss_url TEXT,
	color TEXT DEFAULT NULL,
	show_img TEXT DEFAULT NULL,
	ts TIMESTAMPTZ DEFAULT Now()
);

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	salt TEXT,
	passhash TEXT,
	username TEXT
);

CREATE TABLE episodes (
	id SERIAL PRIMARY KEY,
	show_id INTEGER REFERENCES shows(id),
	episode_url TEXT,
	title TEXT,
	insertion_date TIMESTAMPTZ DEFAULT Now(),
	duration TEXT DEFAULT '00:00:00',
	episode_img TEXT DEFAULT NULL
);

CREATE TABLE user_episode_joins (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users(id),
	episode_id INTEGER REFERENCES episodes(id)
);

CREATE TABLE user_show_joins (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users(id),
	show_id INTEGER REFERENCES shows(id)
)
