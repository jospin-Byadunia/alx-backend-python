import sqlite3

class ExecuteQuery:
    def __init__(self,query,params):
        self.connection = None
        self.cursor = None
        self.query = query
        self.params = params if params is not None else ()
    def __enter__(self):
        self.connection = sqlite3.connect('mydb.sqlite')
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
            print(f"Error: {exc_val}")
        self.cursor.close()
        self.connection.close()