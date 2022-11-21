from flask import Flask, render_template, request, redirect, url_for, flash
import pickle
import requests
API_KEY = "IHCC2UVgUGOMaQFQ-Jeel36IloVaSRfVhJXNVggF3S6y"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)
#model = pickle.load(open('liver.pkl', 'rb'))

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
    #pre=model.predict([[Age,Gender,Total_Bilirubin,Direct_Bilirubin,Alkaline_Phosphotase,Alamine_Aminotransferase,Aspartate_Aminotransferase,Total_Protiens,Albumin,Albumin_and_Globulin_Ratio]])
    #pre=str(pre[0])
    payload_scoring = {"input_data": [{"fields": ['Age', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase',
           'Alamine_Aminotransferase', 'Aspartate_Aminotransferase',
           'Total_Protiens', 'Albumin', 'Albumin_and_Globulin_Ratio','Gender_Male'], "values": [[65,0.7,0.1,187,16,18,6.8,3.3,0.9,1] ]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/94a6cb1f-5f8c-45c1-b65a-54e4960756bf/predictions?version=2022-11-21', json=payload_scoring,
     headers={'Authorization': 'Bearer ' + mltoken})
    #print("Scoring response")
    #print(response_scoring.json())
    pred=response_scoring.json()
    output=pred['predictions'][0]['values'][0][0]
    
    
    if output=="0":
        return render_template("Positive.html")
    else:
        return render_template("Negative.html")



if __name__=="__main__":
    app.run(debug=True)    