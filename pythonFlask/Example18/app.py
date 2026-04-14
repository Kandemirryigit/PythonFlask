from flask import Flask,redirect

app=Flask(__name__)

@app.route("/")
def mainPage():
    return "Main page"

@app.route("/older-page")
def older_page():
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)



# redirect to / when you visit /older-page