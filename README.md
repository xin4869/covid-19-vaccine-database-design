# Project Vaccine Distribution
> Course project - Databases for data science

In this project, I desgined first conceptual UML diagram to describe the relation of different tables. You can find the UML diagram [here](UML/revised.svg). 
Then, I established a connection with the course PostgreSQL Database server using Python and its library psycopg2, which you can see [here](https://github.com/xin4869/covid-19-vaccine-database-design/blob/f16e330f8e00698fd7d1021f6f084cefc2ebe0a0/code/data_to_psql_db.py) from line 65 yo line 83. 

A helper function was defined to read and run SQL files, which can be found [here](https://github.com/xin4869/covid-19-vaccine-database-design/blob/f16e330f8e00698fd7d1021f6f084cefc2ebe0a0/code/data_to_psql_db.py) from line 32 to 62. I wrote a separate SQL file to [create tables](https://github.com/xin4869/covid-19-vaccine-database-design/blob/f16e330f8e00698fd7d1021f6f084cefc2ebe0a0/database/create_and_file_db_psql.sql). then, using this helper function run_sql_from_file(), tables are created. 

After data were read from [csv files](https://github.com/xin4869/covid-19-vaccine-database-design/tree/f16e330f8e00698fd7d1021f6f084cefc2ebe0a0/data), the tables are populated using df.to_sql(). 

All postgreSQL files for data analysis are included in the folder [database](https://github.com/xin4869/covid-19-vaccine-database-design/tree/f16e330f8e00698fd7d1021f6f084cefc2ebe0a0/database)

The last part of the project was analyzing data using Python, which can be found in the python script [data_analysis.py](https://github.com/xin4869/covid-19-vaccine-database-design/blob/f16e330f8e00698fd7d1021f6f084cefc2ebe0a0/code/data_analysis.py).

