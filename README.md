# Tournament Management
Tournament administrator for a variety of games, it supports [Swiss-system tournament][2] that is used for non-elimination format.

# What's included
Within the download you'll find the following directories and files:

```
Tournament-Management-master/
├── tournament.py
├── tournament_test.py
├── database
	└── tournament.sql
```	

# Prerequisites
## Installed software
* `Python 2.7`
* `PostgreSQL 9.0` or higher. View [PostgreSQL Download and Install Instructions][4]
* `Psycopg` adapter. Psycopg is a PostgreSQL adapter for the Python programming language. View [Psycopg Install Instructions][3] 

## Database

### Creating Database
In order to run the program you must create the database named `tournament` using the following sql command:

```
> CREATE DATABASE tournament;
```

### Importing database schema
Once the database is created you must connect to it:

```
> \c tournament;
```
And import `tournament.sql` file with:

```
> \i database/tournament.sql;
```

# Program Execution

# License
[The MIT License (MIT)][1]

[1]: LICENSE
[2]: https://en.wikipedia.org/wiki/Swiss-system_tournament
[3]: http://initd.org/psycopg/docs/install.html
[4]: http://www.postgresql.org/download/