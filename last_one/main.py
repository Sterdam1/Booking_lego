# Писать общую херню

import sqlite3 as sl

# db = sl.connect('last_one\db.sqlite3', check_same_thread=False)


class DataBase:
    def __init__(self):
        global db
        self.db = db
    # Потом подумать зачем мне это нужно 
    def create_sql(self, listy, table_name):
        string = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, "
        for l in range(len(listy)):
            string += listy[l] + ' TEXT' + ', '*(l != len(listy)-1)

        return string+')'

    def drop(self, table_name):
        with self.db as con:
            some_sql = con.execute(f"DROP TABLE {table_name}")

class DataBaseBooking:
    def __init__(self):
        self.db = sl.connect('db_booking.sqlite3')

    def if_table(self, table_name):
        with self.db as con:
            some_sql = con.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        return some_sql.fetchall()

    def create_table(self, listy, table_name):
        string = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, "
        for l in range(len(listy)):
            string += listy[l] + ' TEXT' + ', '*(l != len(listy)-1)
        string += ')'

        with self.db as con:
            some_sql = con.execute(string)
            con.commit()
        
        return some_sql.fetchall()
    
    def get_table(self, table_name):
        with self.db as con:
            some_sql = con.execute(f"PRAGMA table_info('{table_name}')")
            column_names = [i[1] for i in some_sql.fetchall()]
            return table_name, column_names

    def drop(self, table_name):
        with self.db as con:
            some_sql = con.execute(f"DROP TABLE {table_name}")

# db = DataBase()
# db_book = DataBaseBooking()

# with db as con:
#     some_sql = con.execute(create_sql(['name', 'time', 'price'], 'my_table'))


