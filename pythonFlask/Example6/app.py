from flask import Flask

app=Flask(__name__)

@app.route("/hello/<name>")
def hello(name):
    return f"Hello {name}!"

if __name__=="__main__":
    app.run(debug=True)



# <name> takes everything as a string