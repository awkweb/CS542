# CS 542

Fall 2016 database management systems project

## Development

A (somewhat) comprehensive list of commands to get started.

### 1. Setup for Python and Postgres

Run the following command to install all the necessary requirements to run this project. 
```shell
> pip install -r requirements.txt
> virtualenv CS542
```

Go up a directory. When you cd back into the project, the shell should show that it is loading the .env file. Type 'y' to accept and that should automatically activate the virtual environment and set the enviornment variables.

 We are using Postgres for our database and Alembic to migrate and update the schema. To configure the project to use a local Postgres database , open the .env file and change the DATABASE_URL as so,
```
source CS542/Scripts/activate
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://[username]:[password]@localhost/[dbname]"
```

Next, you will need to migrate to update the local database's schema.
```shell
> python manage.py db init
> python manage.py db migrate
> python manage.py db upgrade
```

At this point the database should now be ready to use. You can check that the tables have been loaded successfully into the database by running commands like the following:
```
> psql
postgres=# \c [dbname]
postgres=# \dt
```
This should result in a list of the tables in the database. 

Finally, to get some data loaded into your database, run 

```
postgres=# COPY employee(first, last, address, phone, email, city, state, zipcode) 
postgres=# FROM '/path/to/data/employees.csv' 
postgres=# DELIMITER ',' CSV HEADER;
postgres=# COPY dish(name, desc, cost, category, spicy_level, time_to_cook) 
postgres=# FROM '/path/to/data/dishes.csv' 
postgres=# DELIMITER ',' CSV HEADER;
```

If it isn't clear, the 'path/to/...' is whatever the path to the csv file is. 

To view your sucessfully preloaded data, run

```
postgres=# select * from employee;
```


### 2. Install NPM dependencies, ready for development

```shell
> npm install
> npm start
```

## Build

```shell
> webpack
```

## License

Released under the MIT license. See LICENSE for details.