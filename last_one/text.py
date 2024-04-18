import sqlite3 as sl

db = sl.connect('last_one\db_booking.sqlite3')

def get_table_data(table_name):
    # comment: надо сделать так чтобы человек видел то что сейчас ввел. 
    # то есть табличка идет снизу вверх 
    with db as con:
        some_sql = con.execute(f"SELECT * FROM {table_name}")

    return some_sql.fetchall()

def get_col_names(table_name):
    with db as con:
        some_sql = con.execute(f"PRAGMA table_info('{table_name}')")
        column_names = [i[1] for i in some_sql.fetchall()]
        return column_names

def get_all_tables():
    with db as con:
        table_data = {}
        some_sql = con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        table_names = [sql[0] for sql in some_sql.fetchall()]
    for t in table_names:
        data = get_table_data(t)
        cols = get_col_names(t)
        table_data[t] = {'col_names': cols, 'data': data}
    return table_data

print(get_all_tables())