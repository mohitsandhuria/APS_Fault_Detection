from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from scipy.stats import ks_2samp
import os,sys
import pandas as pd
import numpy as np
from sensor import utils


class DataTransformation:
    def __init__(self,
                    data_transformation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
            try:
                self.data_transformation_config=data_transformation_config
                self.data_ingestion_artifact=data_ingestion_artifact
            except Exception as e:
                raise SensorException(e, sys)

    