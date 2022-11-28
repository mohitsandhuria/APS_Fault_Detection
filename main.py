from sensor.exception import SensorException
from sensor.logger import logging
import sys,os

def test_exception_logger():
     
     try:
          logging.info("Starting the try block")
          result=3/0
          print(result)
          logging.info("stoping the try block")
     except Exception as e:
          logging.info("Starting the Exception block")
          raise SensorException(e, sys)

if __name__=="__main__":
     try:
          test_exception_logger()
     except Exception as e:
          logging.warning(e)
          print(e)
