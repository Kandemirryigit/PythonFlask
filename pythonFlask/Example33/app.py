from flask import Flask,jsonify,request

app=Flask(__name__)

users=[]
next_id=1

@app.route("/users",methods=["GET"])
def list_users():
    return jsonify(users),200

@app.route("/users",methods=["POST"])
def add_user():
    global next_id

    data=request.get_json()

    if not data:
        return jsonify({"error":"You didn't send json"}),400
    
    if "name" not in data or "email" not in data:
        return jsonify({"error":"name and email required"}),400
    
    new_user={
        "id":next_id,
        "name":data["name"],
        "email":data["email"]
    }

    users.append(new_user)
    next_id+=1

    return jsonify(new_user),201



@app.route("/users/<int:id>",methods=["PUT"])
def update_user(id):
    data=request.get_json()

    if not data:
        return jsonify({"error":"You didn't send json"}),400
    
    for user in users:
        if user["id"]==id:
            if "name" in data:
                user["name"]=data["name"]
            if "email" in data:
                user["email"]=data["email"]
            return jsonify(user),200
        
    return jsonify({"error":"user not found"}),404

            

@app.route("/users/<int:id>",methods=["DELETE"])
def delete_user(id):
    for index,user in enumerate(users):
        if user["id"]==id:
            users.pop(index)
            return jsonify({"error":"user deleted"}),200
    return jsonify({"error":"user not found!"}),404





if __name__ == "__main__":
    app.run(debug=True)