import sqlite3
from functools import wraps
from flask import Flask,g,request,jsonify,session,render_template
from werkzeug.security import generate_password_hash,check_password_hash


app=Flask(__name__)
app.secret_key="123"
DATABASE="library101.db"


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




def login_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        if "user_id" not in session:
            return jsonify({"error":"you have to login!"}),401
        return f(*args,**kwargs)
    return decorated







@app.route("/")
def mainPage():
    return render_template("index.html")




@app.route("/api/me",methods=["GET"])
def me():
    if "user_id" not in session:
        return jsonify({"login":False}),200
    return jsonify({"login":True,"email":session["user_email"]}),200




@app.route("/api/register",methods=["POST"])
def register():
    data=request.get_json()
    if not data:
        return jsonify({"error":"There are no json!"}),400
    
    email=data.get("email","")
    password=data.get("password","")

    if not email or "@" not in email:
        return jsonify({"error":"please write a valid email address!"}),400
    if not password or len(password)<6:
        return jsonify({"error":"Password's lenght should be minimum 6 character"}),400
    
    db=get_db()
    try:
        hashed=generate_password_hash(password)
        db.execute("INSERT INTO users (email,password) VALUES (?,?)",(email,hashed))
        db.commit()
        return jsonify({"message":"register successful"}),201
    except sqlite3.IntegrityError:
        return jsonify({"error":"this email already registered!"}),400
    


@app.route("/api/login",methods=["POST"])
def login():
    data=request.get_json()
    if not data:
        return jsonify({"error":"there are no json"}),400
    
    email=data.get("email","")
    password=data.get("password","")

    if not email or not password:
        return jsonify({"error":"Email and password required"}),400
    
    db=get_db()
    user=db.execute(
        "SELECT * FROM users WHERE email=?",(email,)
    ).fetchone()

    if user is None:
        return jsonify({"error":"Email not found!"}),400
    if not check_password_hash(user["password"],password):
        return jsonify({"error":"password is incorrect!"}),400
    
    session["user_id"]=user["id"]
    session["user_email"]=user["email"]
    return jsonify({"message":"login successful!","email":user["email"]}),200



@app.route("/api/exit",methods=["POST"])
def exit():
    session.clear()
    return jsonify({"message":"exit successful!"}),200





@app.route("/api/books",methods=["GET"])
@login_required
def get_books():
    db=get_db()
    books=db.execute(
        "SELECT * FROM books WHERE user_id=?",(session["user_id"],)
    ).fetchall()
    return jsonify([dict(k) for k in books]),200





@app.route("/api/books",methods=["POST"])
@login_required
def add_book():
    data=request.get_json()
    if not data:
        return jsonify({"error":"there are no json!"}),400
    
    name=data.get("name","")
    author=data.get("author","")
    point=data.get("point",0)

    if not name:
        return jsonify({"error":"book name is required!"}),400
    if not author:
        return jsonify({"error":"author is required!"}),400
    if point not in [1,2,3,4,5]:
        return jsonify({"error":"point should be between 1-5"}),400
    
    db=get_db()
    db.execute(
        "INSERT INTO books (name,author,point,user_id) VALUES (?,?,?,?)",
        (name,author,point,session["user_id"])
    )
    db.commit()
    return jsonify({"message":"book added!"}),201




@app.route("/api/books/<int:id>",methods=["PUT"])
@login_required
def update_book(id):
    data=request.get_json()
    if not data:
        return jsonify({"error":"There are no json"}),400
    
    db=get_db()
    book=db.execute(
        "SELECT * FROM books WHERE id=? AND user_id=?",
        (id,session["user_id"])
    ).fetchone()

    if book is None:
        return jsonify({"error":"book couldn't find"}),404
    
    name=data.get("name",book["name"])
    author=data.get("author",book["author"])
    point=data.get("point",book["point"])

    if point not in [1,2,3,4,5]:
        return jsonify({"error":"Point should be between 1-5"}),400
    
    db.execute(
        "UPDATE books SET name=?,author=?,point=? WHERE id=? ",
        (name,author,point,id)
    )
    db.commit()
    return jsonify({"message":"book updated"}),200




@app.route("/api/books/<int:id>",methods=["DELETE"])
@login_required
def delete_book(id):
    db=get_db()
    book=db.execute(
        "SELECT * FROM books WHERE id=? AND user_id=?",
        (id,session["user_id"])
    ).fetchone()

    if book is None:
        return jsonify({"error":"book couldn find"}),404
    
    db.execute("DELETE FROM books WHERE id =?",(id,))
    db.commit()
    return jsonify({"message":"book deleted"}),200




if __name__ == "__main__":
    init_db()
    app.run(debug=True)


