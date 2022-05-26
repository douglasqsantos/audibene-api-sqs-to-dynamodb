# Used to parse .env files
import os
# Used to handle environment variables
from dotenv import load_dotenv
# Used to Handle Logs
import logging

# Loading variables
load_dotenv()

# Logger configuration
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

# Loading AWS Configuration
logger.info(f"Loading AWS Configurations")

# Check Variables
AWS_VARS = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_DEFAULT_REGION', 'AWS_SQS_NAME']
for key in AWS_VARS:
    msg = f"Variable {key} Must be defined"
    if os.getenv(key) == None:
        logger.fatal(msg)
    else:
      if key == "AWS_ACCESS_KEY_ID":
        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
      elif key == "AWS_SECRET_ACCESS_KEY":
        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
      elif key == "AWS_DEFAULT_REGION":
        AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
      elif key == "AWS_SQS_NAME":
        AWS_SQS_NAME = os.getenv("AWS_SQS_NAME")


logger.info(f"AWS Configurations Loaded")


# Check Variables
FLASK_VARS = ['FLASK_HOST','FLASK_PORT', 'FLASK_DEBUG']
for i in FLASK_VARS:
  msg = f"Variable {i} Should be defined. It will have a default value"
  if os.getenv(i) == None:
      logger.warning(msg)

# Loading Flask Configurations
logger.info(f"Loading Flask Configurations")

if os.getenv("FLASK_HOST") == None or os.getenv("FLASK_HOST") == "":
  FLASK_HOST = "0.0.0.0"
  logger.info(f"Variable FLASK_HOST does not has value, initializing with default value: {FLASK_HOST} ")
else:
  FLASK_HOST = os.getenv("FLASK_HOST")

if os.getenv("FLASK_PORT") == None or os.getenv("FLASK_PORT") == "":
  FLASK_PORT = "5000"
  logger.info(f"Variable FLASK_PORT does not has value, initializing with default value: {FLASK_PORT}")
else:
  FLASK_PORT = os.getenv("FLASK_PORT")

if os.getenv("FLASK_DEBUG") == None or os.getenv("FLASK_DEBUG") == "":
  FLASK_DEBUG = False
  logger.info(f"Variable FLASK_DEBUG does not has value, initializing with default value: {FLASK_DEBUG}")
else:
  FLASK_DEBUG = os.getenv("FLASK_DEBUG")

logger.info(f"Flask Configurations Loaded")


# Loading Dynamodb Configurations
logger.info(f"Loading Dynamodb Configurations")

if os.getenv("DYNAMODB_CREDIT_CARD_TABLE") == None or os.getenv("DYNAMODB_CREDIT_CARD_TABLE") == "":
  DYNAMODB_CREDIT_CARD_TABLE = "CreditCard"
  logger.info(f"Variable DYNAMODB_CREDIT_CARD_TABLE does not has value, initializing with default value: {DYNAMODB_CREDIT_CARD_TABLE} ")
else:
  DYNAMODB_CREDIT_CARD_TABLE = os.getenv("DYNAMODB_CREDIT_CARD_TABLE")

if os.getenv("DYNAMODB_PAYPAL_TABLE") == None or os.getenv("DYNAMODB_PAYPAL_TABLE") == "":
  DYNAMODB_PAYPAL_TABLE = "CreditCard"
  logger.info(f"Variable DYNAMODB_PAYPAL_TABLE does not has value, initializing with default value: {DYNAMODB_PAYPAL_TABLE} ")
else:
  DYNAMODB_PAYPAL_TABLE = os.getenv("DYNAMODB_PAYPAL_TABLE")

# Tables
Tables = [DYNAMODB_CREDIT_CARD_TABLE, DYNAMODB_PAYPAL_TABLE]

logger.info(f"Dynamodb Configurations Loaded")