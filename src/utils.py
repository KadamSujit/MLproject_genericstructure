import os
import sys

import numpy as np 
import pandas as pd
import dill #similar like pickle
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

#function for saving an object, takes file path and obj
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path) #dir path
        os.makedirs(dir_path, exist_ok=True) #makes dir

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
#custom function for evaluating various models
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        #looping through model and param list
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            #fit the model with GridSearchCV
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            #train best fit model
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            #model metrics
            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)