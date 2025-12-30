import os
import sys
import pandas as pd
import numpy as np
import json
from pymongo import MongoClient
import certifi
#----------------------------------------------------------
import networksecurity.components.constants as constants
#----------------------------------------------------------
from networksecurity.components.exception import CustomException
from networksecurity.components.logger import ns_logger
#----------------------------------------------------------
ca=certifi.where()
#----------------------------------------------------------
class NetworkDataExtractor:
    def __init__(self):
        self.MONGO_DB_URI = constants.MONGO_DB_URI
        self.NETWORK_DATA_FILE_AND_PATH = constants.network_data_file_and_path
    #----------------------------------------------------------
    def cv_to_json(self, file_path) -> list:
        try:
            data = pd.read_csv(file_path,index_col=False)
            json_data = json.loads(data.to_json(orient="records"))
            return json_data
        except Exception as e:
            raise CustomException(e, sys) from e
    #----------------------------------------------------------
    def push_data_to_mongo(self, data: list, db_name: str, collection_name: str):
        try:
            client = MongoClient(self.MONGO_DB_URI, tlsCAFile=ca)
            db = client[db_name]
            collection = db[collection_name]
            if isinstance(data, list):
                collection.insert_many(data)
                ns_logger.log_info(f"Inserted {len(data)} records into {db_name}.{collection_name}")
            else:
                collection.insert_one(data)
                ns_logger.log_info(f"Inserted 1 record into {db_name}.{collection_name}")
        except Exception as e:
            raise CustomException(e, sys) from e
#----------------------------------------------------------
if __name__ == "__main__":
    try:
        extractor = NetworkDataExtractor()
        json_data = extractor.cv_to_json(extractor.NETWORK_DATA_FILE_AND_PATH)
        print(json.dumps(json_data[:5], indent=4))
        num_of_records = len(json_data) if isinstance(json_data, list) else 1
        print(f"Number of records to be inserted: {num_of_records}")
        extractor.push_data_to_mongo(json_data, db_name="mongodb", collection_name="network_data_collection")
    except Exception as e:
        raise CustomException(e, sys) from e