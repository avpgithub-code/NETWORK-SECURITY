import sys
from networksecurity.components.logger import ns_logger
import networksecurity.components.exception as ns_exception
from networksecurity.components.push_data import NetworkDataExtractor
from networksecurity.components.data_ingestion import DataIngestion
#----------------------------------------------------------
# Assuming MasterConfig is imported from your entity configuration
from networksecurity.entity.config_app import MasterPipelineConfig

def main():
    try:
        # 1. Initialize Master Configuration
        # This single object contains mongodb, ingestion, and training configurations
        master_config = MasterPipelineConfig()
        ns_logger.log_info("Master Configuration initialized.")
        # 2. Data Extraction and MongoDB Push
        ns_logger.log_info("Starting to push network security data to MongoDB - Atlas.")
        # Accessing mongo_config through the master object
        extractor = NetworkDataExtractor(config=master_config.mongodb)
        json_data = extractor.cv_to_json(master_config.mongodb.file_path)
        extractor.push_data_to_mongo(json_data)
        ns_logger.log_info("Data push to MongoDB - Atlas completed successfully.")
        # 3. Data Ingestion
        ns_logger.log_info("Starting data ingestion process.")
        # Passing sub-configs directly from the master_config object
        data_ingestion = DataIngestion(
            mongodb_config=master_config.mongodb,
            ingestion_config=master_config.ingestion,
            train_config=master_config.training_pipeline,
            ingestion_artifact_config=master_config.ingestion_artifact
        )
        data_ingestion.initiate_data_ingestion()
        ns_logger.log_info("Data ingestion and artifact generation completed successfully.")

    except Exception as e:
        raise ns_exception.CustomException(e, sys) from e

if __name__ == "__main__":
    main()