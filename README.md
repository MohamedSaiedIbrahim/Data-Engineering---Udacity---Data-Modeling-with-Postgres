
# Data Engineering Udacity Nanodegree - Project1
## Data Modeling wirth Postgres

### Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

### Project Description
In this project, we'll apply a data modeling with Postgres and build an ETL pipeline using Python. We'll define 1 fact table and 4 dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.

#### Fact Table
1. songplays - records in log data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

#### Dimension Tables
1. users - users in the app
user_id, first_name, last_name, gender, level
2. songs - songs in music database
song_id, title, artist_id, year, duration
3. artists - artists in music database
artist_id, name, location, latitude, longitude
4. time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday

#### Python scripts
We've 2 python scripts that should be included in the main python scripts:
1. sql_queries.py - contains the template for all drop, inserts and create queries
2. create_tables.py - contains the functions to create the DB, create the full tables and drop all tables (utilize the sql_queries.py scripts)

python scripts can be tested using:
1. python CLI
2. IDLE tool

While they are being injected using 2 ways:
1. import as follow:
    from sql_queries import *
    from create_tables import *
2. using run utilities as follow:
    %run -n create_tables
    %run -n sql_queries
    
#### Repository Files
In addition to the data files, the project workspace includes 7 files:

- test.ipynb displays the first few rows of each table to let you check your database.
- create_tables.py drops and creates your tables. You run this file to reset your tables before each time you run your ETL scripts.
- etl.ipynb reads and processes a single file from song_data and log_data and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables.
- etl.py reads and processes files from song_data and log_data and loads them into your tables. You can fill this out based on your work in the ETL notebook.
- sql_queries.py contains all your sql queries, and is imported into the last three files above.
- README.md provides discussion on your project.
- Resulted Schema ERD.PNG final postgres ERD snapshot from pgAdmin

#### DB Schema
As clarified above, It'll be a star schema consists of 1 fact table and 4 dimension tables (please check "Resulted Schema ERD.PNG")

#### ETL pipeline
1. import the required packages
2. Run the Python scripts (Create_tables.py & sql_queries.py) to drop, create the whole tables and define the Insert and Select statments
3. Process song_data files
4. Extract and insert Data for Songs table (1st dimension table)
5. Extract and insert Data for Artist table (2nd dimension table)
6. Process log_data files
7. Extract and insert Data for Time table (3rd dimension table)
8. Extract and insert Data for Users table (4th dimension table)
9. Extract and insert Data for songplays table (fact table)
10. Run test.ipynb to see if you've successfully added records to all tables and check constraints and any warnings inside

