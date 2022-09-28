# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays 
                                (songplay_id SERIAL PRIMARY KEY,
                                start_time TIMESTAMP NOT NULL,
                                user_id int NOT NULL,
                                LEVEL varchar,
                                song_id varchar NOT NULL,
                                artist_id varchar NOT NULL,
                                session_id int,
                                location varchar,
                                user_agent varchar)""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users 
                            (user_id int PRIMARY KEY,
                            first_name varchar,
                            last_name varchar,
                            gender varchar,
                            LEVEL varchar)""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs 
                            (song_id varchar PRIMARY KEY,
                            title varchar NOT NULL,
                            artist_id varchar,
                            YEAR INTEGER,
                            duration NUMERIC NOT NULL)""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists
                            (artist_id varchar PRIMARY KEY,
                            name varchar NOT NULL,
                            location varchar,
                            latitude double precision,
                            longitude double precision)""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time 
                            (start_time TIMESTAMP NOT NULL,
                            HOUR varchar,
                            DAY varchar,
                            week varchar,
                            MONTH varchar,
                            YEAR varchar,
                            weekday varchar)""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT
                                INTO
                                songplays (start_time,
                                user_id,
                                LEVEL,
                                song_id,
                                artist_id,
                                session_id,
                                location,
                                user_agent)
                        VALUES (%s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s)
                        ON CONFLICT DO NOTHING""")

user_table_insert = ("""INSERT
                            INTO
                            users (user_id,
                            first_name,
                            last_name,
                            gender,
                            LEVEL)
                    VALUES (%s,
                            %s,
                            %s,
                            %s,
                            %s)
                    ON CONFLICT (user_id) DO
                    UPDATE
                    SET
                            first_name = EXCLUDED.first_name,
                            last_name = EXCLUDED.last_name,
                            gender = EXCLUDED.gender,
                            LEVEL = EXCLUDED.LEVEL""")

song_table_insert = """INSERT
                            INTO
                            songs (song_id,
                            title,
                            artist_id,
                            YEAR,
                            duration)
                    VALUES (%s,
                    %s,
                    %s,
                    %s,
                    %s)
                    ON CONFLICT DO NOTHING"""

artist_table_insert = ("""INSERT
                            INTO
                            artists (artist_id,
                            name,
                            location,
                            latitude,
                            longitude)
                    VALUES (%s,
                    %s,
                    %s,
                    %s,
                    %s)
                    ON CONFLICT DO NOTHING""")

time_table_insert = ("""INSERT
                            INTO
                            time (start_time,
                            HOUR,
                            DAY,
                            week,
                            MONTH,
                            YEAR,
                            weekday)
                    VALUES (%s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s)""")

# FIND SONGS

song_select = ("""select s.song_id, s.title, s.artist_id, a.name, s.duration from songs s inner join artists a on a.artist_id = s.artist_id""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
