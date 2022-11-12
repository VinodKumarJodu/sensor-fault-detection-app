import os, sys
from sensor.logger import logging
from sensor.exceptions import SensorException
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation

class TrainPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        # self.data_ingestion_config = DataIngestionConfig()
        # self.data_validation_config = DataValidationConfig()
        # self.data_transformation_config = DataTransformationConfig()

    def  start_data_ingestion(self)->DataIngestionArtifact:
        try:
            
            logging.info("Starting Data Ingestion")
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_validation(self,data_ingestion_artifact: DataIngestionArtifact)-> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config= self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact= data_ingestion_artifact, data_validation_config = data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact= data_validation_artifact, data_transformation_config = data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_training(self, data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config) 
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_triainer_artifact = model_trainer.initiate_model_training()
            return model_triainer_artifact
        except Exception as e:
            raise SensorException(e, sys)
    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact, model_trainer_artifact: ModelTrainerArtifact):
        try:
            logging.info("Model Evaluation Started")
            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config = self.training_pipeline_config)
            model_evaluation = ModelEvaluation(model_evaluation_config, data_validation_artifact, model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info("Model Evaluation Completed")
            logging.info(f"model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact= data_validation_artifact)
            model_trainer_artifact = self.start_model_training(data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_validation_artifact, model_trainer_artifact)

            if not model_evaluation_artifact.is_model_accepted:
                raise Exception("Trained Model is not better than the best model")
        except Exception as e:
            raise SensorException(e,sys)
