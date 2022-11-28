import pandas as pd
from sensor.config import mongo_client
from sensor.exception import SensorException
from sensor.logger import logging
import sys,os


def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.dataframe:
    try:
        logging.info("Reading Data from Database {} and Collection {}".format(database_name,collection_name))
        df=pd.DataFrame(list(mongo_client[database_name][collection_name.find()]))
    
    except Exception as e:
        raise SensorException(e, sys)

