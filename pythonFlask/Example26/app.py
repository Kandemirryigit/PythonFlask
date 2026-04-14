import sqlite3
from flask import Flask,g,render_template,request,redirect,session



app=Flask(__name__)
app.secret_key="123"

DATABASE="library.db"



def get_db():
    if "db" not in g:
        g.db=sqlite3.connect(DATABASE)
        g.db.row_factory=sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db=g.pop("db",None)
    if db is not None:
        db.close()


def init_db():
    db=sqlite3.connect(DATABASE)
    db.execute("""
        CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               email TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL
               )
""")
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS books(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               author TEXT NOT NULL,
               point INTEGER NOT NULL,
               user_id INTEGER NOT NULL,
               FOREIGN KEY (user_id) REFERENCES users(id)
               )
""")
    db.commit()
    db.close()






@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    
    email=request.form["email"]
    password=request.form["password"]

    db=get_db()

    try:
        db.execute("INSERT INTO users (email,password) VALUES (?,?)",(email,password))
        db.commit()
        return redirect("/login")
    except sqlite3.IntegrityError:
        return render_template("register.html",error="this email already registered")



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    
    email=request.form["email"]
    password=request.form["password"]

    db=get_db()
    user=db.execute(
        "SELECT * FROM users WHERE email=? AND password=?",(email,password)
    ).fetchone()

    if user is None:
        return render_template("login.html",error="Email or password is wrong")
    
    session["user_id"]=user["id"]
    session["user_email"]=user["email"]
    return redirect("/books")




@app.route("/books")
def books():
    if "user_id" not in session:
        return redirect("/login")
    
    db=get_db()
    books=db.execute(
        "SELECT * FROM books WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    return render_template("/books.html",books=books)






@app.route("/book/add",methods=["GET","POST"])
def book_add():
    if "user_id" not in session:
        return redirect("/login")

    if request.method=="GET":
        return render_template("add_book.html")
    
    name=request.form["name"]
    author=request.form["author"]
    point=request.form["point"]

    db=get_db()
    db.execute(
        "INSERT INTO books (name,author,point,user_id) VALUES (?,?,?,?)",
        (name,author,point,session["user_id"])
    )
    db.commit()
    return redirect("/books")

    




@app.route("/book/<int:id>/delete")
def delete_book(id):
    if "user_id" not in session:
        return redirect("/login")
    
    db=get_db()
    db.execute(
        "DELETE FROM books WHERE id=? AND user_id=? ",
        (id,session["user_id"])
    )
    db.commit()
    return redirect("/books")


@app.route("/exit")
def exit():
    session.clear()
    return redirect("/login")











if __name__ == "__main__":
    init_db()
    app.run(debug=True)