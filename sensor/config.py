import pymongo
import pandas as pd
import json
from dataclasses import dataclass
import os

@dataclass
class EnvironmentVariable:
    mongo_db_url=os.getenv("MONGO_DB_URL")
    aws_secret_key_id=os.getenv("AWS_SECRET_KEY_ID")
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")

env_var=EnvironmentVariable()

mongo_client= pymongo.MongoClient(env_var.mongo_db_url)

DATA_FILE_PATH="/config/workspace/aps_failure_training_set1.csv"
DATABASE_NAME="aps"
COLLECTION_NAME="sensor"
TARGET_COLUMN = "class"