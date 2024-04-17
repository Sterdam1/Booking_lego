# Писать общую херню

import sqlite3 as sl

db = sl.connect('last_one\db.sqlite3', check_same_thread=False)
db_book = sl.connect('last_one\db_booking.sqlite3')

def create_sql(listy, table_name):
    string = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, "
    for l in range(len(listy)):
        string += listy[l] + ' TEXT' + ', '*(l != len(listy)-1)

    return string+')'

def drop(table_name):
    with db as con:
        some_sql = con.execute(f"DROP TABLE {table_name}")

# with db as con:
#     some_sql = con.execute(create_sql(['name', 'time', 'price'], 'my_table'))

# drop('my_table')