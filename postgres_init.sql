CREATE TABLE shows (
	id SERIAL PRIMARY KEY,
	show_title TEXT,
	rss_url TEXT,
	ts TIMESTAMP
);

CREATE TABLE episodes (
	episode_id SERIAL,
	show_id SERIAL REFERENCES shows(id),
	episode_url TEXT,
	episode_title TEXT,
	PRIMARY KEY (show_id, episode_title)
)
