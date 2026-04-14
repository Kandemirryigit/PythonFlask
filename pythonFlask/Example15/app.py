from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    if request.method == "POST":
        message = request.form.get("text")

    return render_template("form.html", message=message)



if __name__=="__main__":
    app.run(debug=True)