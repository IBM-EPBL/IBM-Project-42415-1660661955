from flask import Flask, render_template, request, redirect, url_for, flash
import pickle

app = Flask(__name__)
model = pickle.load(open('liver.pkl', 'rb'))

@app.route("/")
def login():
    return render_template("login.html")
@app.route('/home')
def my_form():    
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
    Age=int(request.form['Age'])
    Gender=int(request.form['Gender'])
    Total_Bilirubin=float(request.form['Total_Bilirubin'])
    Direct_Bilirubin=float(request.form['Direct_Bilirubin'])
    Alkaline_Phosphotase=int(request.form['Alkaline_Phosphotase'])
    Alamine_Aminotransferase=int(request.form['Alamine_Aminotransferase'])
    Aspartate_Aminotransferase=int(request.form['Aspartate_Aminotransferase'])
    Total_Protiens=float(request.form['Total_Protiens'])
    Albumin=float(request.form['Albumin'])
    Albumin_and_Globulin_Ratio=float(request.form['Albumin_and_Globulin_Ratio'])
    pre=model.predict([[Age,Gender,Total_Bilirubin,Direct_Bilirubin,Alkaline_Phosphotase,Alamine_Aminotransferase,Aspartate_Aminotransferase,Total_Protiens,Albumin,Albumin_and_Globulin_Ratio]])
    pre=str(pre[0])
    if pre=="0":
        return render_template("Positive.html")
    else:
        return render_template("Negative.html")



if __name__=="__main__":
    app.run(debug=True)