"""
Utility Functions Module for the Application
This module provides utility functions used across the application,
such as ensuring the existence of directories.
"""
import os
import sys
import pandas as pd
from pathlib import Path
from sklearn import set_config
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
#------------------------------------------------------------------
# Import custom exception and logger
#------------------------------------------------------------------
import networksecurity.components.exception as CustomException
# import src.myproject.logger as logger
import networksecurity.components.constants as constants
#--------------------------------------------------------------------
# Ensure directory exists function
#--------------------------------------------------------------------
test_size = constants.TEST_SIZE
test_size_val = constants.TEST_SIZE_VAL
random_state = constants.RANDOM_STATE
#--------------------------------------------------------------------
def ensure_directory_exists(directory_path):
    """Checks if a directory exists, and creates it if necessary."""
    path = Path(directory_path)
    if not path.exists():
        # Creates the directory and any necessary parent directories
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")
#--------------------------------------------------------------------
# Function to Read data from file
#--------------------------------------------------------------------
def ingest_data_from_file(raw_data: str):
    """
    Function to ingest data from a given file path.
    Raises CustomException on failure.
    """
    try:
        if not os.path.exists(raw_data):
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exception.CustomException(exc_type, exc_value, exc_traceback) from FileNotFoundError(f"The file {raw_data} does not exist.")
        with open(raw_data, 'r', encoding='utf-8') as file:
            df = pd.read_csv(file)
            # logger.app_logger.info("Data ingested successfully from %s", raw_data)
            return df
    except exception.CustomException as ce:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
#--------------------------------------------------------------------
# Train-Test Split Function
#--------------------------------------------------------------------
def train_valid_test_split_data(self, X, y, test_size=test_size, random_state=random_state):
    """Splits the data into training and testing sets."""
    try:
        #--------------------------------------------------
        # 1. First Split: Isolate the final 'Test' set (e.g., 20% of total data)
        # Use 'stratify' to ensure class proportions are kept across splits
        #--------------------------------------------------
        # logger.app_logger.info("Splitting X into X_train_full and X_test...")
        X_train_full, X_test, y_train_full, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        #--------------------------------------------------
        # 3. Second Split: Divide the 'Train-Full' set into 'Train' and 'Validation'
        # To get a 60/20/20 overall split, we take 25% of the remaining 80% (0.25 * 0.80 = 0.20)
        #--------------------------------------------------
        # logger.app_logger.info("Splitting X_train_full into X_train and X_val...")
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_full, y_train_full, test_size=test_size_val, random_state=random_state
        )
        # logger.app_logger.info("Data split completed.")
        return (X_train, y_train), (X_val, y_val), (X_test, y_test)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise exception.CustomException(exc_type, exc_value, exc_traceback) from e
#--------------------------------------------------------------------
# List Dataframe Columns by Type
#--------------------------------------------------------------------
def list_dataframe_columns_by_type(df: pd.DataFrame):
    """
    Returns lists of numerical and character (object/string) column names.
    """
    #----------------------------------------------------
    # 'number' includes both integers and floats
    #----------------------------------------------------
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    if constants.TARGET_COLUMN in numerical_cols:
        numerical_cols.remove(constants.TARGET_COLUMN)
    #----------------------------------------------------
    # 'object' is standard for characters/strings in 2025
    # 'category' is also included for categorical types
    #----------------------------------------------------
    character_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    return numerical_cols, character_cols
#--------------------------------------------------------------------
# Perform Data Transformation Pipelines
#--------------------------------------------------------------------
def create_data_transformation_object(numerical_features, categorical_features) -> ColumnTransformer:
    """
    Creates and returns data transformation pipelines for numerical and categorical features.
    """
    try:
        # logger.app_logger.info("Creating Numerical and Categorical data transformation pipelines...")
        #----------------------------------------------------------------
        # Define transformers for numerical and categorical features
        #----------------------------------------------------------------
        set_config(transform_output="pandas") # Ensures output is a DataFrame
        #----------------------------------------------------------------
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        #----------------------------------------------------------------
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            # Standard: Set sparse_output=False to enable Pandas DataFrame output
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        #----------------------------------------------------------------
        # Combine transformers into a ColumnTransformer
        #----------------------------------------------------------------
        # logger.app_logger.info("Combining transformers into a ColumnTransformer...")
        #----------------------------------------------------------------
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_features),
                ('num', numerical_transformer, numerical_features)
            ],sparse_threshold=0 # Ensures output is a DataFrame
        )
        preprocessor.set_output(transform="pandas") # Ensures output is a DataFrame
        #----------------------------------------------------------------
        # logger.app_logger.info("Data transformation pipelines created successfully.")
        #----------------------------------------------------------------
        return preprocessor
    except Exception as ce:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise exception.CustomException(exc_type, exc_value, exc_traceback) from ce
    
    # def get_project_root():
    # # Searches upward for a specific marker file
    # for parent in Path(__file__).resolve().parents:
    #     if (parent / ".env").exists():
    #         return parent
    # return Path(__file__).resolve().parent  # Fallback