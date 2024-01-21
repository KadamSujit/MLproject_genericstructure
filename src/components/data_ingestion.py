import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass # dataclass is used for creating class variables

'''from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
'''


@dataclass # dataclass is used for creating class variables directly by just giving annotation to the class. It is a decorator.
class DataIngestionConfig: 
    #This is class just for configuration purpose. 
    #When we only need to define variables then use dataclass. If we want to create some methods then go with standard approach.
    #As dataclass is used, all the variables inside are directly initiated as class variables
    #Hence no need to use __init__() or self.
    train_data_path: str=os.path.join('artifacts',"train.csv") #path for train data. All data will be saved in artifact folder
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")



class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig() #ingestion_config has info from all three variables. As in __init__() it becomes a class variable

    #method for ingesting data
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            #reading the data. Here itself we can read data from other sources like mongoDB, API or web, etc
            df=pd.read_csv('notebook\data\stud.csv') 
            logging.info('Read the dataset as dataframe')

            #making dir to save the readed raw data
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) #take dirname
            #saving raw data
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            #creating train and test and saving them
            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True) #save train
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True) #save test
            logging.info("Inmgestion of the data iss completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)
        
# Here, in this class we read the dataset from some location (here local machine), 
# then we saved the data (raw as well as train. test) and then return the saved train, test path.
        
if __name__=="__main__":
    obj=DataIngestion()
    obj.initiate_data_ingestion()

    '''
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
    '''