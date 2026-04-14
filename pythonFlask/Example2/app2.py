from flask import Flask

app=Flask(__name__)

@app.route("/")
def mainPage():
    return "main page"

@app.route("/about")
def about():
    return "about page"

@app.route("/contact")
def contact():
    return "contact page"

@app.route("/admin")
def admin():
    return "admin page"


if __name__=="__main__":
    app.run(debug=True)