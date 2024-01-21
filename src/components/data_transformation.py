import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer #used for creating pipeline
from sklearn.impute import SimpleImputer #to impute values
from sklearn.pipeline import Pipeline #to create pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler #for OHE and normalization

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    #This config gives any path/input the will be required for data transformation components class
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl") #creating pickle file and filepath for data transformation

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig() #initialize class variable from Config class

    def get_data_transformer_object(self):
        '''
        This function is responsible for data trnasformation
        
        '''
        try:
            #numerical features
            numerical_columns = ["writing_score", "reading_score"]
            #categorical features
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # operating on numerical columns
            # creating pipeline with two operations, hangle missing value and data normalization
            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")), #handles missing value by imputing/replacing them with median values
                ("scaler",StandardScaler()) #data normalize

                ]
            )

            # operating on numerical columns
            # creating pipeline with three operations, hangle missing value, OHE and data normalization
            cat_pipeline=Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Numerical columns: {numerical_columns}")
            logging.info(f"Categorical columns: {categorical_columns}")

            # column transformer to combine multiple pipelines
            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns), #input is pipeline name, pipeline and variables
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    # Now starting data transformation
    def initiate_data_transformation(self,train_path,test_path):

        try:
            #reading train and test data
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Read train and test data completed")

            #reading preprocessor object
            logging.info("Obtaining preprocessing object")
            preprocessing_obj=self.get_data_transformer_object() #getting data transformer object

            #seperating dependent and independent variables
            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1) #independent features
            target_feature_train_df=train_df[target_column_name] #dependent features

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            # applying transformation to train and test data
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            # combining dependent and independent features and converting them to array
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # saving data transformer object
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            
            logging.info(f"Saved preprocessing object.")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        
        except Exception as e:
            raise CustomException(e,sys)