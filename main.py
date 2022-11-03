import os, sys
from sensor.logger import logging
from sensor.exceptions import SensorException
from sensor.pipeline.training_pipeline import TrainPipeline

if __name__ == "__main__":
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        # logging.exception(e)
        raise e