from datetime import datetime
import os
from sensor.logger import logging
from dataclasses import dataclass
# Importing training pipeline related constants
from sensor.constants.training_pipeline_constants import PIPELINE_NAME, ARTIFACT_DIR, FILE_NAME, TRAIN_FILE_NAME, TEST_FILE_NAME, MODEL_FILE_NAME
# Importing Data Ingestion related constants
from sensor.constants.training_pipeline_constants import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DIR_NAME, DATA_INGESTION_FEATURE_STORE_DIR, DATA_INGESTION_INGESTED_DIR, DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
# Importing Data Validation Related Constants
from sensor.constants.training_pipeline_constants import DATA_VALIDATION_DIR_NAME, DATA_VALIDATION_VALID_DIR, DATA_VALIDATION_INVALID_DIR, DATA_VALIDATION_DRIFT_REPORT_DIR, DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
# Importing Data Transformation Related Constants
from sensor.constants.training_pipeline_constants import DATA_TRANSFORMATION_DIR_NAME, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR_NAME, DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, PREPROCESSING_OBJECT_FILE_NAME
# Importing Model trainer Constants
from sensor.constants.training_pipeline_constants import MODEL_TRAINER_DIR_NAME, MODEL_TRAINER_TRAINED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_NAME, MODEL_TRAINER_EXPECTED_SCORE, MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD
# Importing Model Evaluation Related COnstants
from sensor.constants.training_pipeline_constants import MODEL_EVALUATION_DIR_NAME, MODEL_EVALUATION_THRESHOLD_SCORE, MODEL_EVALUATION_REPORT_NAME
#Importing Model Pusher Related Constants
from sensor.constants.training_pipeline_constants import MODEL_PUSHER_DIR_NAME, MODEL_PUSHER_SAVED_MODEL_DIR, SAVED_MODEL_DIR
class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.timestamp = timestamp
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, timestamp)


class DataIngestionConfig:
    def __init__(self, training_pipeline_config = TrainingPipelineConfig()):
        self.data_ingestion_dir:str = os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
        self.train_file_path: str = os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
        self.test_fie_path: str = os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = DATA_INGESTION_COLLECTION_NAME

class DataValidationConfig:
    def __init__(self, training_pipeline_config = TrainingPipelineConfig()):
        self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir: str = os.path.join(self.data_validation_dir,DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir,DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, TEST_FILE_NAME)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, TRAIN_FILE_NAME)
        self.invaid_test_file_path: str = os.path.join(self.invalid_data_dir, TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(self.data_validation_dir, DATA_VALIDATION_DRIFT_REPORT_DIR, DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path: str = os.path.join(self.data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR_NAME, TRAIN_FILE_NAME.replace("csv","npy"))
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR_NAME, TEST_FILE_NAME.replace("csv", "npy"))
        self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, PREPROCESSING_OBJECT_FILE_NAME)

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path: str = os.path.join(self.model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR,MODEL_FILE_NAME)
        self.expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD

class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        logging.info("Entered Model Evaluation Config")
        self.model_evaluation_dir: str = os.path.join(training_pipeline_config.artifact_dir, MODEL_EVALUATION_DIR_NAME)
        self.change_threshold: float = MODEL_EVALUATION_THRESHOLD_SCORE
        self.report_file_path: str = os.path.join(self.model_evaluation_dir, MODEL_EVALUATION_REPORT_NAME)
        logging.info("Exited from Model Evaluation Config")

class ModelPusherConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        logging.info("Entered Model Pusher Config")
        self.model_pusher_config = os.path.join(training_pipeline_config.artifact_dir, MODEL_PUSHER_DIR_NAME)
        self.model_file_path = os.path.join(self.model_pusher_config, MODEL_FILE_NAME)
        timestamp = round(datetime.now().timestamp())
        self.saved_model_path = os.path.join(SAVED_MODEL_DIR,f"{timestamp}", MODEL_FILE_NAME)