from sensor.exception import SensorException
import os,sys
from sensor.predictor import ModelResolver
import pandas as pd
from sensor.logger import logging

def batch_prediction(input_file_path):
    try:
        pass
    except Exception as e:
        raise SensorException(e, sys)