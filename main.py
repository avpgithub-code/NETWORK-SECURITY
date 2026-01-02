import sys
import json
import numpy as np
import pandas as pd
#----------------------------------------------------------
# Main Module for Network Security Data Operations
#----------------------------------------------------------
from networksecurity.components.logger import ns_logger
import networksecurity.components.exception as ns_exception
from networksecurity.entity.config_app import MongoDBAtlasConfig
from networksecurity.components.push_data import NetworkDataExtractor
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_app import DataIngestionConfig, TrainingPipelineConfig, DataIngestionArtifact

#----------------------------------------------------------

def main():
    try:
        ns_logger.log_info("Starting to push network security data to MongoDB - Atlas.")
        #----------------------------------------------------------
        # 1. Instantiate 'push_data' Configuration
        #----------------------------------------------------------
        mongo_config = MongoDBAtlasConfig()
        extractor = NetworkDataExtractor(config=mongo_config)
        json_data = extractor.cv_to_json(mongo_config.file_path)
        extractor.push_data_to_mongo(json_data)
        ns_logger.log_info("Data push to MongoDB - Atlas completed successfully.")
        #----------------------------------------------------------
        # 2. Instantiate 'data_ingestion' Configuration
        #----------------------------------------------------------
        ns_logger.log_info("Starting data ingestion from MongoDB - Atlas.")
        ingestion_config = DataIngestionConfig()
        ingestion_artifact = DataIngestionArtifact()
        training_config = TrainingPipelineConfig()
        ingestion_artifact = DataIngestionArtifact()
        ns_logger.log_info("DataIngestionArtifact instantiated successfully.")
        data_ingestion = DataIngestion(mongo_config, ingestion_config, training_config, ingestion_artifact)
        data_ingestion = DataIngestion(mongodb_config=mongo_config,ingestion_config=ingestion_config,
            train_config=training_config,ingestion_artifact=ingestion_artifact
        )
        data_ingestion.initiate_data_ingestion()
        ns_logger.log_info("Data ingestion from MongoDB - Atlas completed successfully.")
    except Exception as e:
        raise ns_exception.CustomException(e, sys) from e

if __name__ == "__main__":
    main()