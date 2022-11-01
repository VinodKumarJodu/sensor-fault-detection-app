from sensor.entity.config_entity import TrainingPipelineConfig
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys


class TrainPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def  start_data_ingestion(self):
        try:
            pass
        except Exception as e:
            rasie SensorException(e, sys)

    def run_pipeline(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
