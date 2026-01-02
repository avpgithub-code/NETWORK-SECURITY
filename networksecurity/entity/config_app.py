from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import networksecurity.components.constants as constants

@dataclass
class MongoDBAtlasConfig:
    """Configuration object to store ingestion metadata."""
    mongo_db_uri: str = constants.MONGO_DB_URI
    mongo_db_name: str = constants.MONGO_DB
    mongo_db_collection_name: str = constants.MONGO_DB_COLLECTION
    file_path: str = constants.NETWORK_DATA_FILE_AND_PATH
    print(f"MongoDBAtlasConfig initialized with URI: {mongo_db_uri}")
    print(f"Database Name: {mongo_db_name}")
    print(f"Collection Name: {mongo_db_collection_name}")
    print(f"File Path: {file_path}")

@dataclass
class DataIngestionConfig():
    """Configuration object for data ingestion."""
    feature_store_dir: Path = constants.DATA_INGESTION_FEATURE_STORE_DIR
    feature_file_name_and_path: Path = constants.FEATURE_FILE_NAME_AND_PATH
    ingested_dir: Path = constants.DATA_INGESTION_INGESTED_DIR
    target_column: str = constants.TARGET_COLUMN
    #----------------------------------------------------------
    train_file_path: Path = constants.DATA_INGESTION_INGESTED_DIR
    train_file_name: Path = constants.TRAIN_FILE_NAME
    test_file_path:Path = constants.DATA_INGESTION_INGESTED_DIR
    train_file_name_and_path: Path = constants.TRAIN_FILE_NAME_AND_PATH
    test_file_name: Path = constants.TEST_FILE_NAME
    test_file_name_and_path: Path = constants.TEST_FILE_NAME_AND_PATH
    #----------------------------------------------------------
    raw_data_file_path: Path = constants.DATA_INGESTION_FEATURE_STORE_DIR
    raw_data_file_name_and_path: Path = constants.FEATURE_FILE_NAME_AND_PATH
    #--------------------------------------------------------
    x_file_path: Path = constants.DATA_INGESTION_FEATURE_STORE_DIR
    x_file_name: Path = constants.X_FILE
    x_file_name_and_path: Path = constants.X_FILE_AND_PATH
    y_file_path: Path = constants.DATA_INGESTION_FEATURE_STORE_DIR
    y_file_name: Path = constants.Y_FILE
    y_file_name_and_path: Path = constants.Y_FILE_AND_PATH
    #----------------------------------------------------------
    x_train_file: str = constants.X_TRAIN_FILE
    x_train_file_and_path: Path = constants.X_TRAIN_FILE_AND_PATH
    y_train_file: str = constants.Y_TRAIN_FILE
    y_train_file_and_path: Path = constants.Y_TRAIN_FILE_AND_PATH
    #----------------------------------------------------------
    x_val_file: str = constants.X_VAL_FILE
    x_val_file_and_path: Path = constants.X_VAL_FILE_AND_PATH
    y_val_file: str = constants.Y_VAL_FILE
    y_val_file_and_path: Path = constants.Y_VAL_FILE_AND_PATH
    #----------------------------------------------------------
    x_test_file: str = constants.X_TEST_FILE
    x_test_file_and_path: Path = constants.X_TEST_FILE_AND_PATH
    y_test_file: str = constants.Y_TEST_FILE
    y_test_file_and_path: Path = constants.Y_TEST_FILE_AND_PATH
    #----------------------------------------------------------
    x_train_transformed_file: str = constants.X_TRAIN_TRANSFORMED_FILE
    x_train_transformed_file_and_path: Path = constants.X_TRAIN_TRANSFORMED_FILE_AND_PATH
    x_val_transformed_file: str = constants.X_VAL_TRANSFORMED_FILE
    x_val_transformed_file_and_path: Path = constants.X_VAL_TRANSFORMED_FILE_AND_PATH
    x_test_transformed_file: str = constants.X_TEST_TRANSFORMED_FILE
    x_test_transformed_file_and_path: Path = constants.X_TEST_TRANSFORMED_FILE_AND_PATH
    #----------------------------------------------------------
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

@dataclass
class DataIngestionArtifact:
    """Configuration object to store artifact paths."""
    train_file_path: Path = constants.DATA_INGESTION_INGESTED_DIR
    train_file_name_and_path: Path = constants.TRAIN_FILE_NAME_AND_PATH
    test_file_path: Path = constants.DATA_INGESTION_INGESTED_DIR
    test_file_name_and_path: Path = constants.TEST_FILE_NAME_AND_PATH
    raw_data_file_path: Path = constants.DATA_INGESTION_FEATURE_STORE_DIR
    raw_data_file_name_and_path: Path = constants.FEATURE_FILE_NAME_AND_PATH
    x_file_path: Path = constants.DATA_INGESTION_FEATURE_STORE_DIR
    x_file_name_and_path: Path = constants.X_FILE_AND_PATH
    y_file_path: Path = constants.DATA_INGESTION_FEATURE_STORE_DIR
    y_file_name_and_path: Path = constants.Y_FILE_AND_PATH
    
# if __name__ == "__main__":
#     mongo_config = MongoDBAtlasConfig()
#     training_config = TrainingPipelineConfig()
#     data_ingestion_config = DataIngestionConfig()
