from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import networksecurity.components.constants as constants

@dataclass
class MongoDBAtlasConfig:
    """Configuration object to store ingestion metadata."""
    mongo_db_uri: str = constants.MONGO_DB_URI
    db_name: str = constants.MONGO_DB
    collection_name: str = constants.MONGO_DB_COLLECTION
    file_path: str = constants.NETWORK_DATA_FILE_AND_PATH
    print(f"MongoDBAtlasConfig initialized with URI: {mongo_db_uri}")
    print(f"Database Name: {db_name}")
    print(f"Collection Name: {collection_name}")
    print(f"File Path: {file_path}")

@dataclass
class DataIngestionConfig():
    """Configuration object for data ingestion."""
    feature_store_dir: Path = constants.DATA_INGESTION_FEATURE_STORE_DIR
    feature_file_name_and_path: Path = constants.FEATURE_FILE_NAME_AND_PATH
    ingested_dir: Path = constants.DATA_INGESTION_INGESTED_DIR
    train_file_name: str = constants.TRAIN_FILE_NAME
    train_file_name_and_path: Path = constants.TRAIN_FILE_NAME_AND_PATH
    test_file_name: str = constants.TEST_FILE_NAME
    test_file_name_and_path: Path = constants.TEST_FILE_NAME_AND_PATH
    train_test_split_ratio: float = constants.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
    test_size:float = constants.TEST_SIZE
    test_size_val: float = constants.TEST_SIZE_VAL
    random_state: int = constants.RANDOM_STATE

@dataclass
class TrainingPipelineConfig:
    """Configuration object for the training pipeline."""
    artifact_dir: Path = constants.ARTIFACT_DIR
    pipeline_name: str = constants.PIPELINE_NAME
    timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")


# if __name__ == "__main__":
#     mongo_config = MongoDBAtlasConfig()
#     training_config = TrainingPipelineConfig()
#     data_ingestion_config = DataIngestionConfig()
