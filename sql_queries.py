import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS stagingEvents"
staging_songs_table_drop = "DROP TABLE IF EXISTS stagingSongs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS stagingEvents
    (artist text,
    auth text,
    firstName text,
    gender text,
    itemInSession INT,
    lastName text,
    length DECIMAL,
    level text,
    location text,
    method text,
    page text,
    registration text,
    sessionId INT,
    song text,
    status INT, 
    ts timestamp,
    userAgent text,
    userId INT)
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS stagingSongs
    (artist_id text,
    artist_latitude DOUBLE PRECISION,
    artist_location text,
    artist_longitude DOUBLE PRECISION,
    artist_name text,
    duration DECIMAL,
    num_songs INT,
    song_id text,
    title text,
    year INT)
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (songplay_id BIGINT IDENTITY(0,1) PRIMARY KEY distkey,
    start_time TIMESTAMP NOT NULL,
    user_id INT NOT NULL,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR ,
    session_id VARCHAR,
    location VARCHAR,
    user_agent VARCHAR)
    diststyle AUTO;
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (user_id INT PRIMARY KEY distkey,
    first_name VARCHAR,
    last_name VARCHAR, 
    gender VARCHAR, 
    level VARCHAR)
    diststyle AUTO;
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs 
    (song_id VARCHAR PRIMARY KEY distkey,
    title VARCHAR NOT NULL,
    artist_id VARCHAR NOT NULL,
    year INT,
    duration DECIMAL NOT NULL)
    diststyle AUTO;
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists 
    (artist_id VARCHAR PRIMARY KEY distkey,
    name VARCHAR NOT NULL, 
    location VARCHAR, 
    latitude DOUBLE PRECISION, 
    longitude DOUBLE PRECISION)
    diststyle AUTO;
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time 
    (start_time TIMESTAMP PRIMARY KEY distkey,
    hour INT,
    day INT, 
    week INT, 
    month INT, 
    year INT, 
    weekday INT)
    diststyle AUTO;
""")

# STAGING TABLES

staging_events_copy = ("""
    copy stagingEvents from ["S3"]["LOG_DATA"]
    ["IAM_ROLE"]["ARN"]
    JSON ["S3"]["LOG_JSONPATH"]
    compupdate off
    timeformat as 'epochmillisecs'
    truncatecolumns blanksasnull emptyasnull;
""").format(["IAM_ROLE"]["ARN"])

staging_songs_copy = """
    copy stagingSongs from ["S3"]["SONG_DATA"]
    ["IAM_ROLE"]["ARN"]
    json 'auto'
    compupdate off;
""".format(["IAM_ROLE"]["ARN"])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays( start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT e.ts, e.userId, e.level, s.song_id, s.artist_id, e.sessionId, e.location, e.userAgent 
    FROM stagingEvents e
    LEFT JOIN stagingSongs s ON e.artist=s.artist_name AND e.length=s.duration AND e.location = s.artist_location AND e.song = s.title
    WHERE e.page = 'NextSong';
""")

user_table_insert = (""" 
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    WITH uniq_staging_events AS (
    SELECT userId, firstName, lastName, gender, level, ROW_NUMBER() OVER(PARTITION BY userid ORDER BY ts DESC) AS rank
    FROM stagingEvents
    WHERE userId IS NOT NULL
    )
    SELECT userId, firstName, lastName, gender, level
    FROM uniq_staging_events
    WHERE rank = 1;
""")

song_table_insert = ("""
    INSERT INTO songs(song_id, title, artist_id, year, duration) 
    SELECT DISTINCT(song_id), title,artist_id, year, duration
    FROM stagingSongs;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT(artist_id), artist_name, artist_location, artist_latitude, artist_longitude
    FROM stagingSongs;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT distinct(ts),
    EXTRACT (HOUR FROM ts),
    EXTRACT (DAY FROM ts),
    EXTRACT (WEEK FROM ts),
    EXTRACT (MONTH FROM ts),
    EXTRACT (YEAR FROM ts), 
    EXTRACT (WEEKDAY FROM ts)
    FROM stagingEvents;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [song_table_insert, artist_table_insert, user_table_insert, time_table_insert, songplay_table_insert]
