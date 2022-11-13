import os, sys
from sensor.logger import logging
from sensor.exceptions import SensorException
from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.entity.artifact_entity import DataValidationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from sensor.ml.metrics.classification_metrics import get_classification_score
from sensor.ml.model.estimator import SensorModel, ModelResolver, TargetValueMapping
from sensor.utils.main_utils import save_object, load_object, write_yaml_file
from sensor.constants.training_pipeline_constants import TARGET_COLUMN
import pandas as pd 

class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig, data_validation_artifact:DataValidationArtifact, model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_evaluation_config = model_evaluation_config
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            logging.info("Entered Model Evaluation Component")
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path 
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path

            # valid train & test dataframe
            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)

            df = pd.concat([train_df, test_df])
            y_true = df[TARGET_COLUMN]
            y_true.replace(TargetValueMapping().to_dict(), inplace=True)
            df.drop(TARGET_COLUMN, axis=1, inplace=True)

            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            model_resolver = ModelResolver()

            is_model_accepted = True
            logging.info(f"The Value of is_model_accepted: {is_model_accepted}")
            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted= is_model_accepted,
                                                                    improved_accuracy= None,
                                                                    best_model_path=None,
                                                                    trained_model_path=trained_model_file_path,
                                                                    trained_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact,
                                                                    best_model_metric_artifact=None)
                logging.info(f"Model Evaluation Artifact: {model_evaluation_artifact}")
                write_yaml_file(self.model_evaluation_config.report_file_path, model_evaluation_artifact.__dict__)
                return model_evaluation_artifact
            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(file_path=latest_model_path)
            train_model = load_object(file_path=trained_model_file_path)

            y_trained_pred = train_model.predict(df)
            y_latest_pred = latest_model.predict(df)
            logging.info(f"y_true: [{y_true}], y_trained_pred: [{y_trained_pred}]")
            trained_metrics = get_classification_score(y_true, y_trained_pred)
            latest_metrics = get_classification_score(y_true,y_latest_pred)

            improved_accuracy = trained_metrics.f1_score - latest_metrics.f1_score
            if self.model_evaluation_config.change_threshold < improved_accuracy:
                is_model_accepted = True
            else:
                is_model_accepted = False

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted = is_model_accepted,
                improved_accuracy = improved_accuracy,
                best_model_path = latest_model_path,
                trained_model_path = trained_model_file_path,
                trained_model_metric_artifact = trained_metrics,
                best_model_metric_artifact = latest_metrics)
            model_evaluation_report = model_evaluation_artifact.__dict__

            # save the report
            write_yaml_file(self.model_evaluation_config.report_file_path, model_evaluation_report)
            logging.info(f"Model Evaluation Artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact   
        except Exception as e:
            raise SensorException(e, sys)