CREATE TABLE shows (
	id SERIAL PRIMARY KEY,
	show_title TEXT,
	rss_url TEXT,
	ts TIMESTAMPTZ DEFAULT Now(),
);

CREATE TABLE episodes (
	episode_id SERIAL,
	show_id INTEGER REFERENCES shows(id),
	episode_url TEXT,
	episode_title TEXT,
	insertion_date TIMESTAMPTZ DEFAULT Now(),
	PRIMARY KEY (show_id, episode_title)
)
