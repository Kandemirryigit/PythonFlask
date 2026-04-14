from flask import Flask,jsonify

app=Flask(__name__)


@app.route("/users/<int:id>")
def users(id):
    users={
        1: {"id": 1, "isim": "Ahmet", "email": "ahmet@test.com"},
        2: {"id": 2, "isim": "Mehmet", "email": "mehmet@test.com"},
    }

    if id not in users:
        return jsonify({"error":"user not found"}),404
    
    return jsonify(users[id]),200


if __name__ == "__main__":
    app.run(debug=True)