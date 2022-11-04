import os
from sensor.constants.s3_bucket import TRAINING_BUCKET_NAME

# Defining Common Constants
TARGET_COLUMN ="class"
PIPELINE_NAME = "sensor"
ARTIFACT_DIR = "artifact"
FILE_NAME = "sensor.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
MODEL_FILE_NAME = "model.pkl"
SCHEMA_FILE_PATH = os.path.join("config","schema.yaml")
SCHEMA_DROP_COLS = "drop_columns"
"""
Defining Data Ingestion Related Constants i.e start with DATA_INGESTION as variable name
"""
DATA_INGESTION_COLLECTION_NAME: str = "sensor"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Defining Data Validation Related Constants & starts with DATA_VALIDATION Variable Name
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "valid_data"
DATA_VALIDATION_INVALID_DIR: str = "invalid_data"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

"""
Defining Data Transformation Reated Constants & starts with DATA_TRANSFORMATION Variable Name
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
