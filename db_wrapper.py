import sqlite3

import db_wrapper_table

class db_wrapper:
    def __init__(self, name="results.db"):
        self.db_name = name
        self.con = None
        self.cursor = None
        self.table_list = {}

    def get_con(self):
        if self.con is None:
            self.con = sqlite3.connect(self.db_name)
            self.con.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
        return self.con

    def get_cursor(self):
        if self.cursor is None:
            self.cursor = self.get_con().cursor()
        return self.cursor

    def add_table(self, table_name):
        self.table_list[table_name] = db_wrapper_table.db_wrapper_table(con=self.get_con(), table_name=table_name)

    def empty_all_dbs(self):
        for table in self.table_list:
            table.empty_db()

    def close_db(self):
        self.get_con().commit()
        self.get_con().close()

    # The following methods are wrappers around the table-specific methods

    def init_table(self, table_name, create_sql):
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].init_db(create_sql)

    def empty_db(self, table_name):
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].empty_db()

    def set_update_sql(self, table_name, update_sql):
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].set_update_sql(update_sql)

    def update_db(self, table_name, params):
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].update_db(params)

    def num_rows(self, table_name):
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].num_rows()

    def print_db(self, table_name):
        if table_name not in self.table_list:
            self.add_table(table_name)
        return self.table_list[table_name].print_db()
