CREATE TABLE shows (
	id SERIAL PRIMARY KEY,
	show_title TEXT,
	rss_url TEXT,
	color TEXT DEFAULT '#ffffff',
	show_img TEXT DEFAULT NULL,
	ts TIMESTAMPTZ DEFAULT Now()
);

CREATE TABLE episodes (
	episode_id SERIAL,
	show_id INTEGER REFERENCES shows(id),
	episode_url TEXT,
	episode_title TEXT,
	insertion_date TIMESTAMPTZ DEFAULT Now(),
	duration TEXT DEFAULT '00:00:00',
	episode_img TEXT DEFAULT NULL,
	PRIMARY KEY (show_id, episode_title)
)
