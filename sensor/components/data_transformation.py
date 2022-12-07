from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from scipy.stats import ks_2samp
import os,sys
import pandas as pd
import numpy as np
from sensor import utils
from sklearn.preprocessing import Pipeline
from sklearn.impute import SimpleImputer
from imblearn.combine import SMOTETomek
from sklearn.preprocessing import RobustScaler
from sensor.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder


class DataTransformation:
    def __init__(self,
                    data_transformation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
            try:
                self.data_transformation_config=data_transformation_config
                self.data_ingestion_artifact=data_ingestion_artifact
            except Exception as e:
                raise SensorException(e, sys)

    @dataclass
    def get_data_transformer(cls):
        try:
            simple_imputer=SimpleImputer(strategy='constant', fill_value=0)
            robust_scaler=RobustScaler()

            constant_pipeline = Pipeline(steps=[
                                        ('Imputer', simple_imputer),
                                        ('RobustScaler', robust_scaler)])

        except Exception as e:
            raise SensorException(e, sys)

    
    def initiate_data_transformation(self):
        try:
            #reading training and testing file
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #selecting input feature for train and test dataframe
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            #selecting target feature for train and test dataframe
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_test_df=test_df[TARGET_COLUMN]

            label_encoder=LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            #transformation on target columns
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            transformation_pipeline = DataTransformation.get_data_transformer()
            transformation_pipeline.fit(input_feature_train_df)

            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            
            smt=SMOTETomek(sampling_strategy="minority")

            logging.info(f"Before resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_arr)
            logging.info(f"After resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            
            logging.info(f"Before resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")
            input_feature_test_arr, target_feature_test_arr = smt.fit_resample(input_feature_test_arr, target_feature_test_arr)
            logging.info(f"After resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")

            train_arr=np.c_[input_feature_train_arr, target_feature_train_arr]
            test_arr=np.c_[input_feature_test_arr, target_feature_test_arr]


            utils.save_numpy_array_data(file_path=self.data_transformation_config.tranformed_train_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.tranformed_test_path, array=test_arr)

            utils.save_object(file_path=self.data_transformation_config.tranform_object_path, 
            obj=transformation_pipeline)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
            obj=label_encoder)

            data_transformation_artifact=artifact_entity.DataTransformationArtifact(
            tranform_object_path=self.data_transformation_config.tranform_object_path, 
            tranformed_train_path=self.data_transformation_config.tranformed_train_path, 
            tranformed_test_path=self.data_transformation_config.tranformed_test_path, 
            target_encoder_path=self.data_transformation_config.target_encoder_path)

            logging.info(f"Data transformation object {data_transformation_artifact}")

        except Exception as e:
            raise SensorException(e, sys)