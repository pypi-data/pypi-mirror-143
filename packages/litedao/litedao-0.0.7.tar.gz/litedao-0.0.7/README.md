**This project is deprecated since the class Database exists in the library [Shared](https://github.com/pyrustic/shared)**

<br><br>

<!-- Intro Text -->
# Litedao
<b> Intuitive interaction with SQLite database </b>

This project is part of the [Pyrustic Ecosystem](https://pyrustic.github.io).

[Installation](#installation) | [Reference](https://github.com/pyrustic/litedao/tree/master/docs/reference#readme) | [Shared](https://github.com/pyrustic/shared)


## Overview
Here is an example of an interaction with an SQL database:

```python
from litedao import Litedao


# Database path (if this file does not exist, it will be created)
DATABASE_PATH = "/home/alex/litedao_test.db"


# SQL code to initialize the database
INIT_SCRIPT = """\
CREATE TABLE friend (username TEXT PRIMARY KEY, email TEXT NOT NULL);
CREATE TABLE enemy (username TEXT PRIMARY KEY, email TEXT NOT NULL)"""


# Insertion SQL code
INSERTION_SQL = """\
INSERT INTO friend (username, email)
VALUES (?, ?), (?, ?)"""


# Selection SQL code
SELECTION_SQL = "SELECT * from friend"


def insert_data(litedao):
    # inserts data in the database then returns a boolean
    return litedao.edit(INSERTION_SQL, param=("alex", "alex@earth.invalid",
                                       "rustic", "rustic@earth.invalid"))


def select_data(litedao):
    # returns the selection
    return litedao.query(SELECTION_SQL)


# litedao instance
litedao = Litedao(DATABASE_PATH, init_script=INIT_SCRIPT)

# insert data if this database is newly created
if litedao.is_new:
    insert_data(litedao)


selection = select_data(litedao)
tables = litedao.tables()
columns = litedao.columns("friend")

litedao.close()  # if you forget to close Litedao, it will close itself at exit

print(selection)
# output: (['username', 'email'], [('alex', 'alex@earth.invalid'), ('rustic', 'rustic@earth.invalid')])

print(tables)
# output: ['friend', 'enemy']

print(columns)
# output: [(0, 'username', 'TEXT', 0, None, 1), (1, 'email', 'TEXT', 1, None, 0)]


```

Read the [reference](https://github.com/pyrustic/litedao/tree/master/docs/reference#readme) !

Do you need to store data collections with another simpler paradigm ? Check [Shared](https://github.com/pyrustic/shared) ! 

## Installation

```bash
pip install litedao
```

