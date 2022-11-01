from datetime import datetime
import os
# Importing training pipeline related constants
from sensor.constants.training_pipeline_constants import PIPELINE_NAME, ARTIFACT_DIR
# Importing Data Ingestion related constants
from sensor.constants.training_pipeline_constants import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DIR_NAME, DATA_INGESTION_FEATURE_STORE_DIR, DATA_INGESTION_INGESTED_DIR, DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.timestamp = timestamp
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, timestamp)


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir:str = os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
        self.feature_store_path: str = os.path.join(self.data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
        self.training_file_path: str = os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR, TRAINING_FILE_NAME)
        self.testing_fie_path: str = os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR, TESTING_FILE_NAME)