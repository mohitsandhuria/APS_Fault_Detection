from dotenv import load_dotenv
from sensor.logger import logging

logging.info("importing environment variables from .env files")

load_dotenv()