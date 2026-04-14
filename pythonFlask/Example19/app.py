from flask import Flask,request

app=Flask(__name__)

@app.route("/inspect")
def inspect():
    return f"""
    Method: {request.method}<br>
    URL: {request.url}<br>
    Path: {request.path}<br>
    Host: {request.host}<br>
    User-Agent: {request.headers.get("User-Agent")}<br>
    """


if __name__ == "__main__":
    app.run(debug=True)