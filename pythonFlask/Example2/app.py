from flask import Flask

app=Flask(__name__)  # Create a Flask app

@app.route("/")   # Define the home page route
def home():
    return "Hello,Flask!"

@app.route("/about")
def about():
    return "This is the about page"


if __name__=="__main__":
    app.run(debug=True)
