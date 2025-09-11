import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Open the database connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor  # return cursor so we can run queries inside `with`

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit if no error, rollback if error
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
            print(f"Error: {exc_val}")
        
        # Close connection
        self.cursor.close()
        self.connection.close()


# First, create a table and insert sample data
with DatabaseConnection("mydb.sqlite") as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))

# Now, query the users table
with DatabaseConnection("mydb.sqlite") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Users in database:")
    for row in results:
        print(row)
# First, create a table and insert sample data
with DatabaseConnection("mydb.sqlite") as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))

# Now, query the users table
with DatabaseConnection("mydb.sqlite") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Users in database:")
    for row in results:
        print(row)