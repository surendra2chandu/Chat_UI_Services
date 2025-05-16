import logging
import os

# Set up logging configuration(Set the logging level to INFO)
logging.basicConfig(level=logging.INFO)

# Get the logger
logger = logging.getLogger()


# Define the database configuration
db_config = {
    "dbname": os.getenv("DB_NAME", "odin_doc_store_dev"),
    "user": os.getenv("DB_USER", "svc_amda"),
    "password": os.getenv("DB_PASSWORD", "fwW8JqRREW3htX"),
    "host": os.getenv("DB_HOST", "ilw-pg.postgres.database.usgovcloudapi.net"),
    "port": 5432,
  }

FOLDER_PATH_ASSIST = os.getenv("DESTINATION_PATH_ASSIST", r"D:\DESTINATION_PATH\ASSIST")
FOLDER_PATH_DAaas = os.getenv("DESTINATION_PATH_DAaas", r"D:\DESTINATION_PATH\DAaas")
FOLDER_PATH_DAaas_How_to = os.getenv("DESTINATION_PATH_DAaas_How_to", r"D:\DESTINATION_PATH\DAaas How to")

categories = {
    "ASSIST": FOLDER_PATH_ASSIST,
    "DAaaS": FOLDER_PATH_DAaas,
    "DAaaS How To": FOLDER_PATH_DAaas_How_to
}
