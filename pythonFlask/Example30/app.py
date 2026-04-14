import sqlite3
from flask import Flask,g,request,render_template,redirect,session,flash
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps


app=Flask(__name__)
app.secret_key="123"

DATABASE="stage4.db"

def required_login(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args,**kwargs)
    return decorated



def get_db():
    if "db" not in g:
        g.db=sqlite3.connect(DATABASE)
        g.db.row_factory=sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
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
    db.commit()
    db.close()




@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    
    email=request.form["email"]
    password=request.form["password"]

    errors=[]

    if not email:
        errors.append("Email cannot be empty!")

    if "@" not in email:
        errors.append("Please write a valid email!")
    
    if not password:
        errors.append("Password cannot be empty!")
    
    if len(password)<6:
        errors.append("The password should be minimum 6 characters!")

    if errors:
        return render_template("register.html",errors=errors)
    
    hashed=generate_password_hash(password)
    db=get_db()
    try:
        db.execute("INSERT INTO users (email,password) VALUES (?,?)",(email,hashed))
        db.commit()
        flash("Registration is successful.You can login")
        return redirect("/login")
    except sqlite3.IntegrityError:
        return render_template("register.html",errors=["This email already registered"])
    




@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    
    email=request.form["email"]
    password=request.form["password"]

    db=get_db()
    user=db.execute(
        "SELECT * FROM users WHERE email=?",(email,)
    ).fetchone()

    if user is None:
        return render_template("login.html",error="We couldn't find this email")
    
    if not check_password_hash(user["password"],password):
        return render_template("login.html",error="Password is wrong")

    session["user_id"]=user["id"]
    session["user_email"]=user["email"]
    return redirect("/profile")





if __name__ == "__main__":
    init_db()
    app.run(debug=True)
