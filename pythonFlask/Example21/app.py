from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def mainPage():
    products=[
        {"name": "Laptop" , "price": 15000},
        {"name": "Phone" , "price": 8000},
        {"name": "Tablet" , "price": 5000},
    ]
    return render_template("index.html",products=products)

    

if __name__ == "__main__":
    app.run(debug=True)