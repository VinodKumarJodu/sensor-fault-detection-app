import os
from sensor.constants.training_pipeline_constants import SAVED_MODEL_DIR, MODEL_FILE_NAME

class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mappiing_response = self.to_dict()
        return dict(zip(mappiing_response.values(), mappiing_response.keys()))


class SensorModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model 
        except Exception as e:
            raise SensorException(e, sys)

    def predict(self, x):
        try:
            X_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(X_transform)
            return y_hat 
        except Exception as e:
            raise SensorException(e, sys)