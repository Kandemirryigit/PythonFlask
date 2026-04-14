from flask import Flask

app=Flask(__name__)

@app.route("/product/<int:product_id>")
def product(product_id):
    return f"Product id: {product_id} - Type: {type(product_id).__name__}"

if __name__=="__main__":
    app.run(debug=True)



# <int:>  just accept integer values not else