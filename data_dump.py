import pymongo
import pandas as pd
import json
import os
from sensor.config import mongo_client


DATA_FILE_PATH="/config/workspace/aps_failure_training_set1.csv"
DATABASE_NAME="aps"
COLLECTION_NAME="sensor"

if __name__=="__main__":
    df=pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and Columns:{df.shape}")

    #converting dataframe to json to dump records in mongodb#
    df.reset_index(drop=True,inplace=True)

    json_record=list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    #inserting into mongodb# 
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)