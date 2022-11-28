import pandas as pd
from sensor.config import mongo_client
from sensor.exception import SensorException
from sensor.logger import logging
import sys,os


def get_collection_as_dataframe(database_name:str,collection_name:str):
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:
        logging.info(f"Reading Data from Database {database_name} and Collection {collection_name}")
        df=pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info("Dropping id column from the dataframe")
            df=df.drop("_id",axis=1)
        logging.info(f"Rows and columns: {df.shape}")
        return df
    except Exception as e:
        raise SensorException(e, sys)

