from flask import Flask,render_template

app=Flask(__name__)

@app.route("/")
def home():
    fruits=["Apple","Banana","Orange"]
    return render_template("index.html",fruits=fruits)


if __name__=="__main__":
    app.run(debug=True)