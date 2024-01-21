import sys
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object

#class for prediction
class PredictPipeline:
    def __init__(self):
        pass

    #predict function used for predicting from the model. takes input as data from which predictions are to be made.
    def predict(self,features):
        try:
            model_path=os.path.join("artifacts","model.pkl") #trained model path
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl') #transfromation obj path
            print("Before Loading")
            #loading all the models
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading")

            #applying transformation on predicting data
            data_scaled=preprocessor.transform(features)
            #predicting from given input data
            preds=model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)


# CustomData is responsible for mapping all the input of html to the backend
class CustomData:
    def __init__(self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):

        self.gender = gender #these values of variables are coming from web application i.e html inputs
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    #our custom fucntion to return all the html input in form of dataframe. Because we have trained our model with dataframe.
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender], #values of dict are from html pages
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)