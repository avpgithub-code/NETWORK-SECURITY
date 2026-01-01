import sys
import numpy as np
import pandas as pd
import certifi
from pymongo import MongoClient
#----------------------------------------------------------
from networksecurity.components import utils
from networksecurity.components.logger import ns_logger
from networksecurity.components.exception import CustomException
from networksecurity.components.constants import MONGO_DB_COLLECTION, MONGO_DB
#----------------------------------------------------------
from networksecurity.entity.config_app import MongoDBAtlasConfig, DataIngestionConfig, TrainingPipelineConfig
#----------------------------------------------------------
class DataIngestion:
    def __init__(self,
                 mongo_config: MongoDBAtlasConfig,
                 ingest_config: DataIngestionConfig,
                 training_config: TrainingPipelineConfig):
        """
        Initialize with DataIngestionConfig and TrainingPipelineConfig.
        """
        try:
            ns_logger.log_info("Initializing DataIngestion with provided configuration.")
            self.mongo_config = mongo_config
            self.training_config = training_config
            self.ingest_config = ingest_config
            #----------------------------------------------------------
            self.db_name = self.mongo_config.mongo_db_name
            self.collection_name = self.mongo_config.mongo_db_collection_name
            #----------------------------------------------------------
            # Initialize MongoDB client for data ingestion
            #----------------------------------------------------------
            ca = certifi.where()
            self.mogo_client = MongoClient(self.mongo_config.mongo_db_uri, tlsCAFile=ca)
            ns_logger.log_info("DataIngestion initialized with provided configuration.")
        except Exception as e:
            raise CustomException(e, sys) from e
    #----------------------------------------------------------
    def read_collection_from_mongo(self) -> pd.DataFrame:
        """Ingest data from the specified file path."""
        try:
            ns_logger.log_info(f"Starting data ingestion from: {MONGO_DB}:{MONGO_DB_COLLECTION}")
            utils.ensure_directory_exists(self.mongo_config.file_path)
            utils.ensure_directory_exists(self.training_config.artifact_dir)
            utils.ensure_directory_exists(self.ingest_config.feature_store_dir)
            utils.ensure_directory_exists(self.ingest_config.ingested_dir)
            #----------------------------------------------------------
            # Ingest data from MongoDB
            #----------------------------------------------------------
            collection = self.mogo_client[self.db_name][self.collection_name]
            collection_df = pd.DataFrame(list(collection.find()))
            #----------------------------------------------------------
            #In 2026, when working with data ingested from MongoDB, 
            # it is a best practice to use a conditional check before dropping the _id column. 
            # This prevents pipeline from crashing if the column is already missing 
            # (e.g., if it was filtered out during the MongoDB query or dropped in a previous step).
            #----------------------------------------------------------
            collection_df.drop(columns=["_id"], axis=1, errors="ignore", inplace=True)
            # Replace multiple variants of "missing" in one go
            collection_df.replace(["na", "NA", "", "nan"], np.nan, inplace=True)
            ns_logger.log_info("Data ingested successfully from MongoDB.")
            #----------------------------------------------------------
            # Derive features (X) and target variable (y)
            #----------------------------------------------------------
            x = collection_df.drop(columns=[self.ingest_config.target_column], axis=1)
            y = collection_df[self.ingest_config.target_column]
            #----------------------------------------------------------
            ns_logger.log_info(f"Features and target variable separated. Features shape: {x.shape}, Target shape: {y.shape}")
            print(f"Features and target variable separated. Features shape: {x.shape}, Target shape: {y.shape}")
            #----------------------------------------------------------
            # Split the data into training, validation, and testing sets
            #----------------------------------------------------------
            (x_train, y_train), (x_val, y_val), (x_test, y_test) = utils.train_valid_test_split_data(x, y)
            ns_logger.log_info("Data split into train, validation, and test sets.")
            ns_logger.log_info(f"Training set shape: {x_train.shape}, Validation set shape: {x_val.shape}, Test set shape: {x_test.shape}")
            print(f"Training set shape: {x_train.shape}, Validation set shape: {x_val.shape}, Test set shape: {x_test.shape}")
            #----------------------------------------------------------
            # Saving the ingested data, Features, and target variable to feature store
            #----------------------------------------------------------
            utils.ensure_directory_exists(self.ingest_config.feature_store_dir)
            collection_df.to_csv(self.ingest_config.feature_file_name_and_path, index=False, header=True)
            x.to_csv(self.ingest_config.x_file_name_and_path, index=False, header=True)
            y.to_csv(self.ingest_config.y_file_name_and_path, index=False, header=True)
            x_train.to_csv(self.ingest_config.x_train_file_and_path, index=False, header=True)
            y_train.to_csv(self.ingest_config.y_train_file_and_path, index=False, header=True)
            x_val.to_csv(self.ingest_config.x_val_file_and_path, index=False, header=True)
            y_val.to_csv(self.ingest_config.y_val_file_and_path, index=False, header=True)
            x_test.to_csv(self.ingest_config.x_test_file_and_path, index=False, header=True)
            y_test.to_csv(self.ingest_config.y_test_file_and_path, index=False, header=True)
            #----------------------------------------------------------
            ns_logger.log_info(f"Ingested data saved to : {self.ingest_config.ingested_dir} and features stored at: {self.ingest_config.feature_store_dir}")
            
            return collection_df,x,y
            #----------------------------------------------------------
            # df = utils.ingest_data_from_file(FILE_NAME_AND_PATH)
            # ns_logger.log_info("Data ingestion completed successfully.")
            # return df
        except Exception as e:
            raise CustomException(e, sys) from e
    #----------------------------------------------------------
    # def split_data(self, df: pd.DataFrame)::
    #     """Split the data into training and testing sets."""
    #     try:
    #         ns_logger.log_info("Starting train-test split.")
    #         X = df.drop(columns=[self.config.target_column], axis=1)
    #         y = df[self.config.target_column]
    #         X_train, X_test, y_train, y_test = utils.train_valid_test_split_data(
    #             X, y,
    #             test_size=self.config.train_test_split_ratio,
    #             random_state=self.config.random_state
    #         )
    #         ns_logger.log_info("Train-test split completed successfully.")
    #         return X_train, X_test, y_train, y_test
    #     except Exception as e:
    #         raise CustomException(e, sys) from e
    #----------------------------------------------------------
    # def save_split_data(self, X_train, X_test, y_train, y_test):
    #     """Save the split data to the specified directories."""
    #     try:
    #         ns_logger.log_info("Saving split data to feature store.")
    #         utils.ensure_directory_exists(self.config.feature_store_dir)

    #         X_train.to_csv(self.config.feature_store_dir / self.config.X_TRAIN_FILE, index=False)
    #         X_test.to_csv(self.config.feature_store_dir / self.config.X_TEST_FILE, index=False)
    #         y_train.to_csv(self.config.feature_store_dir / self.config.Y_TRAIN_FILE, index=False)
    #         y_test.to_csv(self.config.feature_store_dir / self.config.Y_TEST_FILE, index=False)

    #         ns_logger.log_info("Split data saved successfully.")
    #     except Exception as e:
    #         raise CustomException(e, sys) from e
    #----------------------------------------------------------
    # def initiate_data_ingestion(self) -> None:
    #     """Main method to initiate data ingestion process."""
    #     try:
    #         ns_logger.log_info("Initiating data ingestion process.")
    #         df = self.ingest_data()
    #         X_train, X_test, y_train, y_test = self.split_data(df)
    #         self.save_split_data(X_train, X_test, y_train, y_test)
    #         ns_logger.log_info("Data ingestion process completed successfully.")
    #     except Exception as e:
    #         raise CustomException(e, sys) from e
#----------------------------------------------------------
# Example usage (for testing purposes)
if __name__ == "__main__":
    try:
        mongo_config = MongoDBAtlasConfig()
        ingest_config = DataIngestionConfig()
        training_config = TrainingPipelineConfig()
        data_ingestion = DataIngestion(mongo_config, ingest_config, training_config)
        read_collection_df,x,y = data_ingestion.read_collection_from_mongo()
        print(read_collection_df.head())
        
    except Exception as e:
        raise CustomException(e, sys) from e
        