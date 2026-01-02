from dataclasses import dataclass
from pathlib import Path
import networksecurity.components.constants as constants

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