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


# Example usage:
# Setup: create a users table and add some data
with sqlite3.connect("mydb.sqlite") as conn:
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cur.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
        ("Alice", 22),
        ("Bob", 30),
        ("Charlie", 28),
        ("Diana", 24),
    ])
    conn.commit()

# Use ExecuteQuery to run SELECT with parameter
query = "SELECT * FROM users WHERE age > ?"
param = (25,)

with ExecuteQuery("mydb.sqlite", query, param) as results:
    print("Users older than 25:")
    for row in results:
        print(row)
