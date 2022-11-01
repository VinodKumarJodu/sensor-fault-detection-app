from datetime import datetime
import os
from sensor.constants.training_pipeline_constants import PIPELINE_NAME, ARTIFACT_DIR

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.timestamp = timestamp
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, timestamp)

