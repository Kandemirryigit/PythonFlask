from flask import Flask,redirect

app=Flask(__name__)

@app.route("/")
def mainPage():
    return "Main page"

@app.route("/older-page")
def older_page():
    return redirect("https://google.com")

if __name__ == "__main__":
    app.run(debug=True)


# redirect to google.com when you visit /older-page