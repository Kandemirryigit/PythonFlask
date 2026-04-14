from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def mainPage():
    products=["Laptop","Phone","Tablet","Keyboard","Computer"]
    return render_template("index.html",products=products)


if __name__ == "__main__":
    app.run(debug=True)