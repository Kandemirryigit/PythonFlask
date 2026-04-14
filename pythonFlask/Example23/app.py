import sqlite3
from flask import Flask,g

app=Flask(__name__)

def get_db():
    if "db" not in g:
        g.db=sqlite3.connect("database.db")
        g.db.row_factory=sqlite3.Row
    return g.db



@app.teardown_appcontext
def close_db(error):
    db=g.pop("db",None)
    if db is not None:
        db.close()




@app.route("/")
def mainPage():
    db=get_db()
    return "Database created successfully"




if __name__ == "__main__":
    app.run(debug=True)










# g is a special Flask object.
# g means global for the current request
# It stores data that lives only during one request

# Example
# User visits /login
# Flask creates a request → g exists → request ends → g disappears.
# So this line checks:
#“Do we already have a database connection stored in g?”
# If not, we create one.








# g.db.row_factory = sqlite3.Row
# Normally SQLite returns tuples:
# (1, "Yiğit", 20)
# But with sqlite3.Row, you can access columns by name:
# row["name"]
# row["age"]
# Instead of:
# row[1]
# row[2]
# This is much cleaner in Flask apps.




