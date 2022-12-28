# Project: Cloud Data Warehouse

### Introduction
---
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

Building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights into what songs their users are listening to. Test database and ETL pipeline by running queries given by the analytics team from Sparkify and compare results with their expected results.

### Project Description
---
In this project, will build an ETL pipeline for a database hosted on Redshift. will load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

### Project Datasets
---
Will working with two datasets that reside in S3. Here are the S3 links for each:

Song data: s3://udacity-dend/song_data
Log data: s3://udacity-dend/log_data
Log data json path: s3://udacity-dend/log_json_path.json

#### Song Dataset
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are file paths to two files in this dataset.

song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json

#### Log Dataset
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate app activity logs from an imaginary music streaming app based on configuration settings.

The log files in the dataset are partitioned by year and month. For example, here are file paths to two files in this dataset.

log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json

### Schema for Song Play Analysis
---
Using the song and event datasets, need to create a star schema optimized for queries on song play analysis. This includes the following tables.

#### Fact Table:
 > - songplays - records in event data associated with song plays i.e. records with page NextSong
     (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
     
#### Dimension Tables:
 > - users - users in the app
     (user_id, first_name, last_name, gender, level)
     
 > - songs - songs in music database
     (song_id, title, artist_id, year, duration)
     
 > - artists - artists in music database
     (artist_id, name, location, lattitude, longitude)
     
 > - time - timestamps of records in songplays broken down into specific units
     (start_time, hour, day, week, month, year, weekday)
     

### Project Template
---
The project template includes three files:

 1- create_table.py is where the fact and dimension tables for the star schema in Redshift created.
 2- etl.py is where data from S3 will be loaded into staging tables on Redshift and then process that data into analytics tables on Redshift.
 3- sql_queries.py is where SQL statements defined, which will be imported into the two other files above.
 
### Project Steps 
---
Below are steps to complete this project.

#### Create Table Schemas 
    1- Design schemas for fact and dimension tables
    2- Write a SQL CREATE statement for each of these tables in sql_queries.py
    3- Complete the logic in create_tables.py to connect to the database and create these tables
    4- Write SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist.
    5- Launch a redshift cluster and create an IAM role that has read access to S3.
    6- Add redshift database and IAM role info to dwh.cfg.
    7- Test by running create_tables.py and checking the table schemas in redshift database. 
    
#### Build ETL Pipeline
    Implement the logic in etl.py to load data from S3 to staging tables on Redshift.
    Implement the logic in etl.py to load data from staging tables to analytics tables on Redshift.
    Test by running etl.py after running create_tables.py and running the analytic queries on Redshift database.
    Delete redshift cluster when finished.
    