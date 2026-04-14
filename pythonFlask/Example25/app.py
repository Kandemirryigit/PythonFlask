import sqlite3
from flask import Flask,g,request,render_template,redirect

app=Flask(__name__)

def get_db():
    if "db" not in g:
        g.db=sqlite3.connect("Database11.db")
        g.db.row_factory=sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db=g.pop("db",None)
    if db is not None:
        db.close()


def init_db():
    db=sqlite3.connect("Database11.db")
    db.execute("""
            CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               email TEXT UNIQUE NOT NULL
               )
""")
    db.commit()
    db.close()



@app.route("/",methods=["GET","POST"])
def mainPage():
    if request.method=="GET":
        return render_template("form.html")
    
    name=request.form["name"]
    email=request.form["email"]

    db=get_db()
    try:
        db.execute("INSERT INTO users (name,email) VALUES (?,?)",(name,email))
        db.commit()
        return redirect("/")
    except sqlite3.IntegrityError:
        return render_template("form.html",error="This email is already registered")
    

    
    


@app.route("/users")
def users_list():
    db=get_db()
    all_users=db.execute("SELECT * FROM users").fetchall()
    return render_template("list.html",users=all_users)



@app.route("/user/<int:id>")
def user_profile(id):
    db=get_db()
    user=db.execute("SELECT * FROM users WHERE id=? ",(id,)).fetchone()
    return render_template("profile.html",user=user)




@app.route("/user/<int:id>/edit",methods=["GET","POST"])
def edit(id):
    db=get_db()
    user=db.execute("SELECT * FROM users WHERE id=? ",(id,)).fetchone()

    if request.method=="GET":
        return render_template("edit.html",user=user)
    
    name=request.form["name"]
    email=request.form["email"]

    try:
        db.execute("UPDATE users SET name=? ,email=? WHERE id=? ",(name,email,id))
        db.commit()
        return redirect("/users")
    except sqlite3.IntegrityError:
        return render_template("edit.html",user=user,error="This email already registered")





@app.route("/user/<int:id>/delete")
def delete(id):
    db=get_db()
    db.execute("DELETE FROM users WHERE id=?",(id,))
    db.commit()
    return redirect("/users")



if __name__=="__main__":
    init_db()
    app.run(debug=True)

