from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from scipy.stats import ks_2samp
import os,sys
import pandas as pd
import numpy as np
from sensor import utils
from xgboost import XGBClassifier
from sklearn.metrics import f1_score

class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
    data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def train_model(self,x,y):
        try:
            xgb_clf =  XGBClassifier()
            xgb_clf.fit(x,y)
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_trainer(self,):
        try:
            logging.info(f"Loading train and test array.")
            train_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.tranformed_train_path)
            test_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.tranformed_test_path)

            logging.info(f"Splitting input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            logging.info(f"Train the model")
            model=self.train_model(x=x_train, y=y_train)
            
            logging.info(f"Calculating f1 train score")
            yhat_train=model.predict(x_train)
            f1_train_score  =f1_score(y_true=y_train, y_pred=yhat_train)

            logging.info(f"Calculating f1 test score")
            yhat_test = model.predict(x_test)
            f1_test_score  =f1_score(y_true=y_test, y_pred=yhat_test)


        except Exception as e:
            raise SensorException(e, sys)