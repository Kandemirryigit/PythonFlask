from flask import Flask,render_template,request,session
import random


app=Flask(__name__)
app.secret_key="key123"

@app.route("/",methods=["GET","POST"])
def game():
    if "number" not in session:
        session["number"]=random.randint(1,10)

    message=""

    if request.method=="POST":
        guess=int(request.form.get("guess"))
        number=session["number"]

        if guess==number:
            message="Correct! New number generated"
            session["number"]=random.randint(1,10)
        elif guess<number:
            message="low"
        else:
            message="High"
        
    return render_template("game.html",message=message)




if __name__ == "__main__":
    app.run(debug=True)