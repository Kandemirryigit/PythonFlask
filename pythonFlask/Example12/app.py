from flask import Flask,render_template,request

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("number.html")


@app.route("/check",methods=["POST"])
def check():
    number=int(request.form.get("number"))
    if number % 2==0:
        result="Even"
    else:
        result="Odd"
    return render_template("number.html",result=result)



if __name__=="__main__":
    app.run(debug=True)