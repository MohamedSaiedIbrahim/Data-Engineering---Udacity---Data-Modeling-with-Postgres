import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from create_tables import *


def process_song_file(cur, filepath):
    """
    process the song files, extract songs and artist DF to be inserted into the final tables
    
    This function simply recieve the song file with connection cursor
    
    Parameters
    ----------
    cur : cursor
        postgres connection cursor.
    filepath : file
        file to be processed.
    
    Returns
    -------
    no return
    
    """
    
    print(filepath)
    # open song file
    df = pd.DataFrame([pd.read_json(filepath, typ='series')])
    print(df.shape)
    
    #  Mostly duration double value will cause a problem. then it's better to convert into string
    df['duration'] = df['duration'].astype('str') 
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']] 
    print(song_data)
    
    # insert song record
    song_data = song_data.values.tolist() 
    for row in song_data:
        cur.execute(song_table_insert, row)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values.tolist() 
    print(artist_data[0:3]) 
    
    for row in artist_data:
        cur.execute(artist_table_insert, row)

def process_log_file(cur, filepath):  
    """
    process the log files, extract time, users and songPlay DF to be inserted into the final tables
    
    This function simply recieve the log file with connection cursor
    
    Parameters
    ----------
    cur : cursor
        postgres connection cursor.
    filepath : file
        file to be processed.
    
    Returns
    -------
    no return
    
    """
    # open log file
    df = pd.concat([pd.read_json(filepath, lines = 'true')])

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']
    df = df.reset_index()
    print(len(df))
	
	# Same as duration, length field to be converted into string
    df['length'] = df['length'].astype('str')

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    time_df = pd.DataFrame() 
    time_df['start_time'] = df['ts'] 
    time_df['hour'] = pd.DatetimeIndex(df['ts']).hour 
    time_df['day'] = pd.DatetimeIndex(df['ts']).day 
    time_df['week'] = pd.DatetimeIndex(df['ts']).week 
    time_df['month'] = pd.DatetimeIndex(df['ts']).month 
    time_df['year'] = pd.DatetimeIndex(df['ts']).year 
    time_df['dayofweek'] = pd.DatetimeIndex(df['ts']).dayofweek
    print(time_df)
    
	# insert time data records
    time_data = time_df.values.tolist()
    column_labels = list(time_df.columns)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']] 
    print(len(user_df))
	
	# First: Strip the log data and delete the null user id entries 
    #user_df=user_df[user_df['userId'] != '']
    user_df = user_df[~user_df['userId'].isnull()]
    
    cols = user_df.columns
    for col in cols:
        user_df[col] = user_df[col].astype(str).str.strip()
		
	# Second: Delete duplications as found alot of them
	# Found alot of duplications
    user_df = user_df.drop_duplicates(subset=['userId']) 
    user_df = user_df.dropna(subset=['userId']) 
    print(len(user_df))

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
	# First, prepare song_select results and delete the duplications
    cur.execute(song_select) 
    song_artist_tuble = cur.fetchall() 
    count = 0 
    for row in song_artist_tuble [0:5]:
        print(row)
		
	# Second, Remove duplications and convert length numeric value to string
    song_artist_df = pd.DataFrame(song_artist_tuble, columns=['song_id', 'song', 'artist_id', 'artist', 'length']) 
    song_artist_df = song_artist_df.drop_duplicates() 
    song_artist_df['length'] = song_artist_df['length'].astype('str') 
    print(len(song_artist_df)) 
    
    # Third: Merging the Song-Artist DF with log files DF 
    all_df = pd.merge(song_artist_df, df, on=['song', 'artist']) 
    all_df = all_df[['ts', 'userId', 'level', 'song_id', 'artist_id', 'sessionId', 'location', 'userAgent']] 
    print(len(all_df)) 
    print(all_df) 
    
    # Forth: Converting the ts into timestamp and renaming some fields 
    song_play_df = all_df.copy() 
    song_play_df.rename(columns = {'ts':'start_time',
									'userId': 'user_Id',
									'sessionId':'session_id',
									'userAgent':'user_agent'}, inplace = True) 
    song_play_df['start_time'] = pd.to_datetime(song_play_df['start_time'], unit='ms') 
    print(len(song_play_df))
	
	#Fifth: Add songplay_id primary key (sequence) 
    #song_play_df = song_play_df.reset_index() 
    #song_play_df = song_play_df.rename(columns={"index":"songplay_id"}) 
    #song_play_df['songplay_id'] = song_play_df.index + 1 
    #print(song_play_df)
    
    songplay_data = song_play_df.values.tolist()
	
	# Finally insert into songplays table:
    for index, row in song_play_df.iterrows():
        cur.execute(songplay_table_insert, list(row)) 
		
    #for index, row in df.iterrows():
    #    
    #    # get songid and artistid from song and artist tables
    #    cur.execute(song_select, (row.song, row.artist, row.length))
    #    results = cur.fetchone()
    #    
    #    if results:
    #        songid, artistid = results
    #    else:
    #        songid, artistid = None, None
	#
    #    # insert songplay record
    #    songplay_data = 
    #    cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    General fun to collect and iterate processing json files
    
    This function simply recieve the log file with connection cursor
    
    Parameters
    ----------
    conn: DB connection object
        postgres connection object
    cur : cursor
        postgres connection cursor.
    filepath : path
        relative path to the json files
    
    Returns
    -------
    no return
    
    Calls
    -----
    func: function
        Calls either process_song_file or process_log_file functions
    
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=student")
    cur = conn.cursor()
	
	#Drop and Create the full tables
    drop_tables(cur, conn) 
    create_tables(cur, conn)

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()