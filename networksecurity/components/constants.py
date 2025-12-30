from pathlib import Path
from dotenv import load_dotenv
import os
#----------------------------------------------------------
load_dotenv()
ROOT_DIR = Path.cwd()
network_data_dir = ROOT_DIR / 'network_data'
network_data_file_and_path = network_data_dir / os.getenv("load_file_to_mongo")
MONGO_DB_URI = os.getenv("MONGO-DB-URI")
#----------------------------------------------------------
if __name__ == "__main__":
    print(f"Network Data Path: {network_data_file_and_path}")