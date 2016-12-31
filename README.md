# CS 542

Fall 2016 database management systems project: split restaurant bills.

![Orders Dashboard](screenshots/01.png)

![New Order](screenshots/02.png)

![Drag & Drop Split](screenshots/03.png)

![View Bill](screenshots/04.png)

## Install & Setup

A (somewhat) comprehensive list of commands to get started.

### 1. Create Postgres database (see [Loading Test Data](https://github.com/tmm/CS542#loading-test-data) for more)

### 2. Setup Python

```shell
> virtualenv -p path/to/python3.5 CS542
> pip install -r requirements.txt
```

### 3. Add .env file

```shell
source CS542/Scripts/activate
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://[username]:[password]@localhost/[dbname]"
```

### 4. Sync DB with Flask models

```shell
> cd server
> python manage.py db init
> python manage.py db migrate
> python manage.py db upgrade
```

### 5. Install NPM dependencies

```shell
> npm install
```
### 6. Build & run the project

```shell
> npm run build
> cd server
> python manage.py runserver
```

## Loading test data

At this point the database should now be ready to use. You can check that the tables have been loaded successfully into the database by running commands like the following:

```shell
> psql
postgres=# \c [dbname]
postgres=# \dt
```

This should result in a list of the tables in the database. 

Finally, to get some data loaded into your database, run 

```shell
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

## License

Released under the MIT license. See LICENSE for details.