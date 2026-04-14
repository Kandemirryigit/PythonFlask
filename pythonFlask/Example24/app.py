import sqlite3
from flask import Flask,g

app=Flask(__name__)

def get_db():
    if "db" not in g:
        g.db=sqlite3.connect("Database10.db")
        g.db.row_factory=sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db=g.pop("db",None)
    if db is not None:
        db.close()


def init_db():
    db=sqlite3.connect("Database10.db")
    db.execute("""
            CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               emial TEXT UNIQUE NOT NULL
               )
""")
    db.commit()
    db.close()
    print("Table created")



@app.route("/")
def mainPage():
    return "MainPage"



if __name__=="__main__":
    init_db()
    app.run(debug=True)