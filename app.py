from flask import Flask, render_template,request 
import product_model

app=Flask(__name__)
@app.route("/", methods=['GET','POST'])
def index():
    result=None
    if request.method =="POST":
        product=request.form['product']
        product_v=product_model.test(product)
        result=product_model.result(product_v)
       
    return render_template("Find_Product.html", result=result)

if __name__ =="__main__":
    app.run(debug=True)