import sys
import numpy as np
import pandas as pd
import certifi
from pymongo import MongoClient
#----------------------------------------------------------
from networksecurity.components import constants, utils
from networksecurity.components.logger import ns_logger
from networksecurity.components.exception import CustomException
#----------------------------------------------------------
from networksecurity.entity.config_app import MongoDBAtlasConfig, \
    DataIngestionConfig, TrainingPipelineConfig, DataIngestionArtifact
#----------------------------------------------------------
class DataIngestion:
    def __init__(
            self,
            mongodb_config: MongoDBAtlasConfig,
            ingestion_config: DataIngestionConfig,
            train_config: TrainingPipelineConfig,
            ingestion_artifact: DataIngestionArtifact
        ):
        """
        Initialize with DataIngestionConfig and TrainingPipelineConfig.
        """
        try:
            ns_logger.log_info("Initializing DataIngestion with provided configuration.")
            self.mongodb_config = mongodb_config
            self.train_config = train_config
            self.ingestion_config = ingestion_config
            #----------------------------------------------------------
            self.db_name = self.mongodb_config.mongo_db_name
            self.collection_name = self.mongodb_config.mongo_db_collection_name
            #----------------------------------------------------------
            # Initialize MongoDB client for data ingestion
            #----------------------------------------------------------
            ca = certifi.where()
            self.mongo_client = MongoClient(self.mongodb_config.mongo_db_uri, tlsCAFile=ca)
            ns_logger.log_info("DataIngestion initialized with provided configuration.")
        except Exception as e:
            raise CustomException(e, sys) from e
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiates the data ingestion process from MongoDB.
        """
        try:
            ns_logger.log_info("Starting data ingestion process from MongoDB.")
            #----------------------------------------------------------
            read_collection_df,x,y = utils.read_collection_from_mongo(
                self.mongodb_config,
                self.train_config,
                self.ingestion_config,
                self.mongo_client, 
                self.db_name, 
                self.collection_name
            )
            ns_logger.log_info("Data read from MongoDB collection successfully.")
            ns_logger.log_info(f"Data shape from MongoDB: {read_collection_df.shape}")
            ns_logger.log_info(f"Features shape: {x.shape}, Target shape: {y.shape}")
            #----------------------------------------------------------
            train_data, test_data = utils.train_test_split_data(
                read_collection_df, 
                self.ingestion_config.test_size,
                self.ingestion_config.random_state
            )
            ns_logger.log_info("Train-test split completed.")
            ns_logger.log_info(f"Train data shape: {train_data.shape}, Test data shape: {test_data.shape}")
            #----------------------------------------------------------
            # Saving train and test data to respective file paths
            #----------------------------------------------------------
            utils.save_train_test_data(self.ingestion_config,train_data,test_data)
            ns_logger.log_info(f"Train data saved to : {self.ingestion_config.train_file_name_and_path}")
            ns_logger.log_info(f"Test data saved to : {self.ingestion_config.test_file_name_and_path}")
            #----------------------------------------------------------
            ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.ingestion_config.train_file_path,
                train_file_name_and_path=self.ingestion_config.train_file_name_and_path,
                test_file_path=self.ingestion_config.test_file_path,
                test_file_name_and_path=self.ingestion_config.test_file_name_and_path,
                raw_data_file_path=self.ingestion_config.raw_data_file_path,
                raw_data_file_name_and_path=self.ingestion_config.raw_data_file_name_and_path,
                x_file_path=self.ingestion_config.x_file_path,
                x_file_name_and_path=self.ingestion_config.x_file_name_and_path,
                y_file_path=self.ingestion_config.y_file_path,
                y_file_name_and_path=self.ingestion_config.y_file_name_and_path
            )
            ns_logger.log_info("Data ingestion process completed successfully.")
            return ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
#----------------------------------------------------------
# Example usage (for testing purposes)
#----------------------------------------------------------
if __name__ == "__main__":
    try:
        ns_logger.log_info("Starting data ingestion process from MongoDB.")
        #----------------------------------------------------------
        mongo_config = MongoDBAtlasConfig()
        ingest_config = DataIngestionConfig()
        training_config = TrainingPipelineConfig()
        ingest_artifact = DataIngestionArtifact()
        data_ingestion = DataIngestion(mongo_config, ingest_config, training_config, ingest_artifact)
        #----------------------------------------------------------
        # Initiate data ingestion and retrieve the data ingestion artifacts
        #----------------------------------------------------------
        ingest_artifact = data_ingestion.initiate_data_ingestion()
        print(ingest_artifact)
    except Exception as e:
            raise CustomException(e, sys) from e
        