from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os
#----------------------------------------------------------
load_dotenv(find_dotenv())
ROOT_DIR = Path.cwd()
network_data_dir = ROOT_DIR / 'network_data'
network_data_file_and_path = network_data_dir / os.getenv("load_file_to_mongo")
MONGO_DB=os.getenv("MONGO-DB")
MONGO_DB_COLLECTION=os.getenv("MONGO-DB-COLLECTION")
MONGO_DB_SUFFIX = os.getenv("MONGO-DB-URI-SUFFIX")
MONGO_DB_URI = os.getenv("MONGO-DB-URI")
#----------------------------------------------------------
if __name__ == "__main__":
    print(f"Network Data Path: {network_data_file_and_path}")
    print(f"MongoDB Suffix: {MONGO_DB_SUFFIX}")
    print(f"MongoDB URI: {MONGO_DB_URI}")