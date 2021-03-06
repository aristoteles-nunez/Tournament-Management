#Table of Contents

- [Tournament Management](#tournament-management)
	- [Features](#features)
	- [ToDo](#todo)
- [What's included](#whats-included)
- [Prerequisites](#prerequisites)
	- [Installed software](#installed-software)
	- [Database](#database)
- [Program Execution](#program-execution)
	- [Running test cases](#running-test-cases)
- [License](#license)


# Tournament Management

Tournament administrator for a variety of games, it supports [Swiss-system tournament][2] that is used for non-elimination format like chess tournaments.

## Features
* **Player registration for future use**. Every player registers once and can be used in every Tournament event.
* **Events**. We can register more than one tournament. 
* **Points earned**. Every player in a match can earn any number of points. It's useful for games where it is allowed tie, because we can add 0.5 points to each player, or stablish our own scale.
* **Avoid rematch between players**. Every player is paired avoiding rematch between them.
* **Support odd number of players**. If there is an odd number of players, a 'Bye' player is added. 
* **Pairing stored for every round**. Each pairing is stored on database with each player's score for that round.

## ToDo
* Rank players according to OMW (Opponent Match Wins).
* Web interface for each funcionallity.


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

In order to run the program you must import database schema

First move to proper directory

```
cd path-to/Tournament-Management-master/
```

Ingress to database and import `tournament.sql` file with:

```
> \i database/tournament.sql;
```
**Note:** You must be in the same system directory where all the files are, in this case, you must be inside of `Tournament-Management-master` folder. The tournament.sql will create the required database.

# Program Execution


## Running test cases
In order to execute all the test cases run:

```
python tournament_test.py 
```

After all cases run successfully, it must shows you the following message:

```
Success!  All tests pass!
```

If there is any problem verify that you accomplish with all pre-requisites.

# License


[The MIT License (MIT)][1]

[1]: LICENSE
[2]: https://en.wikipedia.org/wiki/Swiss-system_tournament
[3]: http://initd.org/psycopg/docs/install.html
[4]: http://www.postgresql.org/download/