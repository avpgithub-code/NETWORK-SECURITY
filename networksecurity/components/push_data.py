import os
import sys
import pandas as pd
import json
import certifi
from pymongo import MongoClient
#----------------------------------------------------------
# Local imports
#----------------------------------------------------------
from networksecurity.components.logger import ns_logger
from networksecurity.components.exception import CustomException
from networksecurity.components.config_app import MongoDBAtlasConfig
#----------------------------------------------------------
# Initialize Certifi for 2025 TLS standards
#----------------------------------------------------------
ca = certifi.where()
#----------------------------------------------------------
# Core Logic
#----------------------------------------------------------
""" Class to handle data extraction and pushing to MongoDB."""
class NetworkDataExtractor:
    def __init__(self, config: MongoDBAtlasConfig):
        """
        Inject the configuration object and initialize the persistent client.
        """
        try:
            self.config = config
            # Connection pooling optimization: init client once
            self.client = MongoClient(self.config.mongo_db_uri, tlsCAFile=ca)
            ns_logger.log_info("MongoDB Client initialized successfully.")
        except Exception as e:
            raise CustomException(e, sys) from e
    #----------------------------------------------------------
    def cv_to_json(self, file_path: str) -> list:
        """Converts CSV data to a list of dictionaries (2025 optimized)."""
        try:
            data = pd.read_csv(file_path, index_col=False)
            # Optimized: Avoid string serialization, use to_dict directly
            return data.to_dict(orient="records")
        except Exception as e:
            raise CustomException(e, sys) from e
    #----------------------------------------------------------
    def push_data_to_mongo(self, data: list):
        """Pushes data using the settings from the config object."""
        try:
            db = self.client[self.config.db_name]
            collection = db[self.config.collection_name]

            if not data:
                ns_logger.log_warning("Empty dataset received. Aborting push.")
                return 0

            # Use ordered=False for parallel insertion performance
            result = collection.insert_many(data, ordered=False)
            count = len(result.inserted_ids)
            
            ns_logger.log_info(f"Inserted {count} records into {self.config.db_name}")
            return count
        except Exception as e:
            raise CustomException(e, sys) from e
#----------------------------------------------------------
# Execution Block
#----------------------------------------------------------
if __name__ == "__main__":
    try:
        #----------------------------------------------------------
        # 1. Instantiate the Configuration
        #----------------------------------------------------------
        ingestion_mongo_config = MongoDBAtlasConfig()
        #----------------------------------------------------------
        # 2. Instantiate the Logic with the Config injected
        extractor = NetworkDataExtractor(config=ingestion_mongo_config)
        #----------------------------------------------------------
        # 3. Execution
        json_data = extractor.cv_to_json(ingestion_mongo_config.file_path)
        #----------------------------------------------------------
        # Debug: Print first 5 records to verify
        #----------------------------------------------------------
        print("--- Data Preview (First 5 Records) ---")
        print(json.dumps(json_data[:5], indent=4))
        print(f"Total Records Prepared: {len(json_data)}")
        #----------------------------------------------------------
        # 4. Push to MongoDB
        #----------------------------------------------------------
        extractor.push_data_to_mongo(json_data)
        
    except Exception as e:
        raise CustomException(e, sys) from e