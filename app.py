from flask import Flask,render_template,request,jsonify
import requests
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl','rb'))
@app.route('/',methods = ['GET'])
def Home():
    return render_template('index.html')
@app.route("/predict",methods = ['POST'])
def predict():
    if request.method == 'POST':
        Year = int(request.form['Year'])
        no_year = 2024 - Year
        Present_Price = int(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol =  int(request.form['Fuel_Type_Petrol'])
        if  Fuel_Type_Petrol  == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif Fuel_Type_Petrol == 'Diesel':
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
        Seller_type_individual = int(request.form['Seller_type_individual'])
        if Seller_type_individual == 'Individual':
            Seller_type_individual = 1
        else:
            Seller_type_individual = 0
        Transmission_Manual = int(request.form['Transmission_Manual'])
        if Transmission_Manual == 'Manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0
        prediction = model.predict([[Present_Price,no_year,Kms_Driven,Owner,Fuel_Type_Petrol,Fuel_Type_Diesel,Seller_type_individual,Transmission_Manual]])
        output = round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry, you cannot sell this car")
        else:
            return render_template('index.html',prediction_texts="You can sell this car at {}".format(output))
    else:
        return render_template('index.html')

if __name__== "__main__":
    app.run(debug=True)