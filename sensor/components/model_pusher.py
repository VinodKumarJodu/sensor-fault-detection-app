import shutil
import os, sys
from sensor.logger import logging
from sensor.exceptions import SensorException
from sensor.entity.config_entity import ModelEvaluationConfig, ModelPusherConfig
from sensor.entity.artifact_entity import ModelTrainerArtifact,ModelEvaluationArtifact, ModelPusherArtifact
from sensor.ml.metrics.classification_metrics import get_classification_score
from sensor.utils.main_utils import save_object, load_object, write_yaml_file

class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact, model_pusher_config:ModelPusherConfig):
        try:
            self.model_evaluation_artifact = model_evaluation_artifact
            self.model_pusher_config = model_pusher_config 
        except Exception as e:
            raise SensorException(e, sys)
    
    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            trained_model_path = self.model_evaluation_artifact.trained_model_path

            # creating model pusher dir to save model
            model_file_path = self.model_pusher_config.model_file_path
            model_dir = os.path.dirname(model_file_path)
            os.makedirs(model_dir, exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)

            # saved model dir
            saved_model_path = self.model_pusher_config.saved_model_path
            model_dir = os.path.dirname(saved_model_path)
            os.makedirs(model_dir, exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)

            # prepare artifact
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path, model_file_path=model_file_path)
            logging.info(f"Model Pusher Artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)