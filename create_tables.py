import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
    
    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=student")
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    drop_table_queries = ['DROP TABLE IF EXISTS songplays',
                          'DROP TABLE IF EXISTS users',
                          'DROP TABLE IF EXISTS songs',
                          'DROP TABLE IF EXISTS artists',
                          'DROP TABLE IF EXISTS time']
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    create_table_queries = ['CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL PRIMARY KEY, start_time TIMESTAMP NOT NULL, user_id int NOT NULL, level varchar, song_id varchar NOT NULL, artist_id varchar NOT NULL, session_id int, location varchar, user_agent varchar)',
                            'CREATE TABLE IF NOT EXISTS users (user_id int PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar)',
                            'CREATE TABLE IF NOT EXISTS songs (song_id varchar PRIMARY KEY, title varchar NOT NULL, artist_id varchar, year INTEGER, duration NUMERIC NOT NULL)',
                            'CREATE TABLE IF NOT EXISTS artists (artist_id varchar PRIMARY KEY, name varchar NOT NULL, location varchar, latitude double precision, longitude double precision)',
                            'CREATE TABLE IF NOT EXISTS time (start_time TIMESTAMP NOT NULL, hour varchar, day varchar, week varchar, month varchar, year varchar, weekday varchar)']
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
