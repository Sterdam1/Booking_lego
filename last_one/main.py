# Писать общую херню

import sqlite3 as sl

# db = sl.connect('last_one\db.sqlite3', check_same_thread=False)
table_data = []


class DataBase:
    def __init__(self):
        global db
        self.db = db
    # Потом подумать зачем мне это нужно 
    def create_sql(self, listy, table_name):
        string = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, "
        for l in range(len(listy)):
            string += listy[l] + ' TEXT' + ', '*(l != len(listy)-1)

        return string+'is_taken INTEGER)'

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
        string += ', is_taken INTEGER)'

        with self.db as con:
            some_sql = con.execute(string)
            con.commit()
        
        return some_sql.fetchall()
    
    def edit_table_row(self, table_name, id, data):
        with self.db as con:
            col_names = ', '.join(self.get_col_names(table_name)[1:])
            format_data = ', '.join([f"'{d}'" for d in data])
            some_sql = con.execute(f"UPDATE {table_name} SET ({col_names}) = ({format_data}) WHERE id = {id}")

    def delete_row(self, table_name, id):
        with self.db as con:
            some_sql = con.execute(f"DELETE FROM {table_name} WHERE id = {id}")

    def get_table_data(self, table_name):
        # comment: надо сделать так чтобы человек видел то что сейчас ввел. 
        # то есть табличка идет снизу вверх 
        with self.db as con:
            some_sql = con.execute(f"SELECT * FROM {table_name}")

        return some_sql.fetchall()

    def get_col_names(self, table_name):
        with self.db as con:
            some_sql = con.execute(f"PRAGMA table_info('{table_name}')")
            column_names = [i[1] for i in some_sql.fetchall()]
            return column_names

    def get_all_tables(self):
        with self.db as con:
            table_data = {}
            some_sql = con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
            table_names = [sql[0] for sql in some_sql.fetchall()]
        for t in table_names:
            data = self.get_table_data(t)
            cols = self.get_col_names(t)
            table_data[t] = {'col_names': cols, 'data': data}

        return table_data

    def insert_info(self, table_name, data):
        with self.db as con:
            col_names = ', '.join(self.get_col_names(table_name)[1:])
            format_data = ', '.join([f"'{d}'" for d in data])
            some_sql = con.execute(f"INSERT INTO {table_name} ({col_names}) VALUES ({format_data})")

    def drop(self, table_name):
            with self.db as con:
                some_sql = con.execute(f"DROP TABLE {table_name}")
                
    
# db = DataBase()
# db_book = DataBaseBooking()

# with db as con:
#     some_sql = con.execute(create_sql(['name', 'time', 'price'], 'my_table'))


