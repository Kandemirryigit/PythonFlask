from flask import Flask,render_template,request

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("calc.html")

@app.route("/calculate",methods=["POST"])
def calculator():
    num1=int(request.form.get("num1"))
    num2=int(request.form.get("num2"))
    result=num1+num2
    return f"Result is {result}"


if __name__=="__main__":
    app.run(debug=True)
