import sqlite3

class db_wrapper_table:
    def __init__(self, con, table_name="transactions"):
        self.table_name = table_name
        self.con = con
        self.cursor = None
        self.delete_sql = "DELETE FROM {0}"
        self.create_sql = None
        self.update_sql = None

    def get_con(self):
        return self.con

    def get_cursor(self):
        if self.cursor is None:
            self.cursor = self.get_con().cursor()
        return self.cursor

    def init_db(self, create_sql):
        cur = self.get_cursor()
        cur.execute(create_sql.format(self.table_name))
        self.get_con().commit()

    def empty_db(self):
        self.get_cursor().execute(self.delete_sql)
        self.get_con().commit()

    def set_update_sql(self, update_sql):
        self.update_sql = update_sql

    def update_db(self, params):
        if self.update_sql == None:
            raise RuntimeError("Call set_update_sql() first")
        cur = self.get_cursor()
        self.get_cursor().execute(self.update_sql.format(self.table_name), params)
        self.get_con().commit()

    def num_rows(self):
        cur = self.get_cursor().execute("SELECT COUNT(*) from {0}".format(self.table_name))
        return cur.fetchone()[0]

    def print_db(self):
        cur = self.get_cursor().execute("SELECT * from {0}".format(self.table_name))
        rows = cur.fetchall()
        for row in rows:
            print row

    def close_db(self):
        self.get_con().commit()
        self.get_con().close()
