import sys
import pandas as pd
from networksecurity.components.constants import FILE_NAME_AND_PATH
from networksecurity.entity.config_app import MongoDBAtlasConfig, DataIngestionConfig, TrainingPipelineConfig
from networksecurity.components.logger import ns_logger
from networksecurity.components.exception import CustomException
from networksecurity.components import utils
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
            ns_logger.log_info("DataIngestion initialized with provided configuration.")
        except Exception as e:
            raise CustomException(e, sys) from e
    #----------------------------------------------------------
    def ingest_data(self) -> pd.DataFrame:
        """Ingest data from the specified file path."""
        try:
            ns_logger.log_info(f"Starting data ingestion from: {FILE_NAME_AND_PATH}")
            utils.ensure_directory_exists(self.mongo_config.file_path)
            utils.ensure_directory_exists(self.training_config.artifact_dir)
            utils.ensure_directory_exists(self.ingest_config.feature_store_dir)
            utils.ensure_directory_exists(self.ingest_config.ingested_dir)
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
        data_ingestion.ingest_data()
    except Exception as e:
        print(f"Error during data ingestion: {e}")
        