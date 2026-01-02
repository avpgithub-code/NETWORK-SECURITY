from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os
#----------------------------------------------------------------------------------------------------
def get_project_root() -> Path:
    #------------------------------------------------------------------------------------------------
    """Finds the project root by searching for a marker file.
    Start from the current file's location and move upwards until a marker file is found.
    Markers can be .env, .git, or pyproject.toml
    Returns: Path object representing the project root directory
    """
    for parent in Path(__file__).resolve().parents:
        # Markers commonly used in 2025: .env, .git, or pyproject.toml
        if (parent / ".env").exists() or \
            (parent / "pyproject.toml").exists() or \
            (parent / ".git").exists():
            return parent

    return Path(__file__).resolve().parent
#----------------------------------------------------------------------------------------------------
# 1. Establish the Anchor Paths for Root, Raw Data, and Processed Data
#----------------------------------------------------------------------------------------------------
ROOT_DIR = get_project_root()
#----------------------------------------------------------
load_dotenv(find_dotenv())
#----------------------------------------------------------
NETWORK_DATA_DIR = ROOT_DIR / 'network_data'
NETWORK_DATA_FILE_AND_PATH = NETWORK_DATA_DIR / os.getenv("LOAD-DATA-FILE-TO-MONGO")
MONGO_DB=os.getenv("MONGO-DB")
MONGO_DB_COLLECTION=os.getenv("MONGO-DB-COLLECTION")
MONGO_DB_SUFFIX = os.getenv("MONGO-DB-URI-SUFFIX")
MONGO_DB_URI = os.getenv("MONGO-DB-URI")
#----------------------------------------------------------
DATA_INGESTION_DB_NAME = os.getenv("MONGO-DB")
DATA_INGESTION_COLLECTION_NAME = os.getenv("MONGO-DB-COLLECTION")
#----------------------------------------------------------
ARTIFACT_DIR = ROOT_DIR / 'artifact'
#----------------------------------------------------------
DATA_INGESTION_DIR = ARTIFACT_DIR / 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR = DATA_INGESTION_DIR / 'feature_store'
DATA_INGESTION_INGESTED_DIR = DATA_INGESTION_DIR / 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION = float(os.getenv("TRAIN-TEST-SPLIT-RATION"))
#----------------------------------------------------------
FILE_NAME=os.getenv("LOAD-DATA-FILE-TO-MONGO", "phisingData.csv")
RAW_FILE_NAME=os.getenv("RAW-FILE-NAME", "raw_data.csv")
FEATURE_FILE_NAME_AND_PATH = DATA_INGESTION_FEATURE_STORE_DIR / RAW_FILE_NAME
TRAIN_FILE_NAME = "train.csv"
TRAIN_FILE_NAME_AND_PATH = DATA_INGESTION_INGESTED_DIR / TRAIN_FILE_NAME
TEST_FILE_NAME = "test.csv"
TEST_FILE_NAME_AND_PATH = DATA_INGESTION_INGESTED_DIR / TEST_FILE_NAME
#----------------------------------------------------------------------------------------------------
# 3. Model Training Constants
TARGET_COLUMN = os.getenv("TARGET-COLUMN", "Result")
PIPELINE_NAME = "network_security_pipeline"
FILE_NAME_AND_PATH = DATA_INGESTION_FEATURE_STORE_DIR / FILE_NAME
#----------------------------------------------------------------------------------------------------
# 4. Other Constants
#----------------------------------------------------------------------------------------------------
TEST_SIZE = float(os.getenv("TEST_SIZE"))
TEST_SIZE_VAL = float(os.getenv("TEST_SIZE_VAL"))
RANDOM_STATE = int(os.getenv("RANDOM_STATE"))
LOG_FILE_MAX_BYTES = int(os.getenv("LOG_FILE_MAX_BYTES")) # 10 MB
LOG_FILE_BACKUP_COUNT = int(os.getenv("LOG_FILE_BACKUP_COUNT")) # 5 backups
#----------------------------------------------------------------------------------------------------
DATA_PROCESSED_FILE = "data.csv"
X_FILE = "X.csv"
X_FILE_AND_PATH = DATA_INGESTION_FEATURE_STORE_DIR / X_FILE 
Y_FILE = "y.csv"
Y_FILE_AND_PATH = DATA_INGESTION_FEATURE_STORE_DIR / Y_FILE
#------------------------------------------------------------------------------------
X_TRAIN_FILE = "X_train.csv"
X_TRAIN_FILE_AND_PATH = DATA_INGESTION_INGESTED_DIR / X_TRAIN_FILE
Y_TRAIN_FILE = "y_train.csv"
Y_TRAIN_FILE_AND_PATH = DATA_INGESTION_INGESTED_DIR / Y_TRAIN_FILE
#------------------------------------------------------------------------------------
X_VAL_FILE = "X_val.csv"
X_VAL_FILE_AND_PATH = DATA_INGESTION_INGESTED_DIR / X_VAL_FILE
Y_VAL_FILE = "y_val.csv"
Y_VAL_FILE_AND_PATH = DATA_INGESTION_INGESTED_DIR / Y_VAL_FILE
#------------------------------------------------------------------------------------
X_TEST_FILE = "X_test.csv"
X_TEST_FILE_AND_PATH = DATA_INGESTION_INGESTED_DIR / X_TEST_FILE
Y_TEST_FILE = "y_test.csv"
Y_TEST_FILE_AND_PATH = DATA_INGESTION_INGESTED_DIR / Y_TEST_FILE
#------------------------------------------------------------------------------------
X_TRAIN_TRANSFORMED_FILE = "X_train_transformed.csv"
X_TRAIN_TRANSFORMED_FILE_AND_PATH = DATA_INGESTION_INGESTED_DIR / X_TRAIN_TRANSFORMED_FILE
X_VAL_TRANSFORMED_FILE = "X_val_transformed.csv"
X_VAL_TRANSFORMED_FILE_AND_PATH = DATA_INGESTION_INGESTED_DIR / X_VAL_TRANSFORMED_FILE
X_TEST_TRANSFORMED_FILE = "X_test_transformed.csv"
X_TEST_TRANSFORMED_FILE_AND_PATH = DATA_INGESTION_INGESTED_DIR / X_TEST_TRANSFORMED_FILE
JOBLIB_FILE = "preprocessor.joblib"
#----------------------------------------------------------------------------------------------------
# Example usage (for testing purposes)
#----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Project Root Directory: {ROOT_DIR}")
    print(f"Network Data Path: {NETWORK_DATA_FILE_AND_PATH}")
    print(f"MongoDB Suffix: {MONGO_DB_SUFFIX}")
    print(f"MongoDB URI: {MONGO_DB_URI}")