from flask import Flask,request

app=Flask(__name__)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return "This is a GET request"
    
    if request.method=="POST":
        return "This is a POST request"
    


if __name__ == "__main__":
    app.run(debug=True)
    
