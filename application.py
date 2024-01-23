from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application=Flask(__name__) #flask app works as a entry point

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') #render template takes to the index/home html location

#route for prediction
@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html') #if method is GET then go to default home page
    else:
        data=CustomData( #get prediction data from html
            gender=request.form.get('gender'), # when we use post method, request has all the information
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))

        )
        #getting prediction input data in form of dataframe
        pred_df=data.get_data_as_data_frame()
        print("Before Prediction")
        print(pred_df)

        predict_pipeline=PredictPipeline() #initializing prediction pipeline
        print("Mid Prediction Details")
        results=predict_pipeline.predict(pred_df) #predicting
        print("Results After Prediction")
        print(results)
        return render_template('home.html',results=results[0])
    

if __name__=="__main__":
    app.run(host="0.0.0.0")        