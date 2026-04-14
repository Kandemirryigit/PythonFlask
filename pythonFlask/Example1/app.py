from flask import Flask

app=Flask(__name__)  # Create a flask app

@app.route("/")  # Define the home page route
def home():
    return "Hello,Flask"


if __name__=="__main__":
    app.run(debug=True)   # Run the app in debug mode



# debug=True means:
# automatically reloads when you change the code.