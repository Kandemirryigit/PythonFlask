from flask import Flask,jsonify

app=Flask(__name__)

@app.route("/user")
def user():
    data={
        "id":1,
        "name":"kandemir",
        "email":"kandemirryigit@gmail.com"
    }
    return jsonify(data)


@app.route("/users")
def users():
    data=[
        {"id":1,"name":"kandemir"},
        {"id":2,"name":"Mehmet"},
        {"id":3,"name":"Ayşe"},
    ]
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)

    