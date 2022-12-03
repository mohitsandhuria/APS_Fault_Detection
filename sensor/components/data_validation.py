from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from scipy.stats import ks_2samp
import os,sys
import pandas


class DataValidation:

    def __init__(self,data_validation_config:config_entity.DataValidationConfig):
        try:
            logging.info(f"{'>>'*20} Data Validation {'>>'*20}")
            self.data_validation_config=data_validation_config
            self.validation_error=dict()
        except Exception as e:
            raise SensorException(e, sys)

    def drop_missing_columns(self,df):

        '''This function will drop the column which contains missing values more than specified threshold
        df : pandas Accepts dataframe
        threshhold: percentage criteria to drop a column
        ===============================================================================================

        Returns pandas dataframe if atleast one column is having the 
        '''

        try:
            threshold=self.data_validation_config.missing_threshold
            null_report=df.isnull().sum()/df.shape[0]
            drop_column_names=null_report[null_report>threshold].index
            self.validation_error['dropped_columns']=drop_column_names
            df.drop(list(drop_column_names),axis=1,inplace=True)

            if len(df.columns)==0:
                return None
            return df
        except Exception as e:
            raise SensorException(e, sys)


    def is_required_column_exists(self,base_df,current_df):
        try:
            missing_columns=[]
            base_columns=base_df.columns
            current_columns=current_df.columns

            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)


            if len(missing_columns)>0:
                self.validation_error["Missing_column"]=missing_columns
                return False
            return False
        except Exception as e:
            raise SensorException(e, sys)


    def data_drift(self,base_df,current_df):
        try:
            drift_report=dict()
            base_columns=base_df.columns
            current_columns=current_df.columns

            for base_column in base_columns:
                base_data,current_data=base_df[base_column],current_df[base_column]
                ###Null hypothesis is that both column drawn same distribution####
                same_distribution=ks_2samp(base_data,current_data)

                if same_distribution.pvalue>0.05:
                    drift_report[base_column]={
                        "pvalue":same_distribution.pvalue,
                        "same_distribution":True}
                else:
                    drift_report[base_column]={
                        "pvalue":same_distribution.pvalue,
                        "same_distribution":False}

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self):
        try:
            pass

        except Exception as e:
            raise SensorException(e, sys)


    