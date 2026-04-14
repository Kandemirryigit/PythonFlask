from flask import Flask,request

app=Flask(__name__)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return """
                <form method="POST">
                <input name="email" placeholder="email">
                <button type="submit">Send</button>
                </form>
                """
    
    if request.method=="POST":
        email=request.form["email"]
        return f"Post came! Email: {email}"
    


if __name__ == "__main__":
    app.run(debug=True)
