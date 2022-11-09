import os, sys
from sensor.logger import logging
from sensor.exceptions import SensorException
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from sensor.utils.main_utils import load_numpy_array_data
from sensor.ml.metrics.classifiaction_metrics import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import save_object, load_object
from xgboost import XGBClassifier

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact 
        except Exception as e:
            raise SensorException(e, sys)
    def train_model(self, X_train, y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(X_train, y_train)
            return xgb_clf 
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_training(self)-> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # loading train and test array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train,y_train, X_test, y_test = (train_arr[:,:-1], train_arr[:,-1], test_arr[:,:-1], test_arr[:,-1])

            model = sef.train_model(X_train, y_train)
            y_train_pred = model.predict(X_train)
            classifiaction_train_metrics = get_classification_score(y_true=y_train, y_pred=y_train_pred)

            if classifiaction_train_metrics.f1_score <= self.model_trainer_config.expected_accuracy:
                raise Exception("Trained Model is not good to provide Expected Accuracy")

            y_test_pred = model.predict(X_test)
            classification_test_metrics = get_classification_score(y_true = y_test, y_pred = y_test_pred)

            # Overfitting & Underfitting 
            diff = abs(classifiaction_train_metrics.f1_score - classification_test_metrics.f1_score)

            if diff > self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model is not good try to do more experimentation")

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
            sensor_model = SensorModel(preprocessor=preprocessor, model=model)
            save_object(self.model_trainer_config.trained_model_file_path, obj=sensor_model)

            # model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classifiaction_train_metrics,
            test_metric_artifact=classification_test_metrics)

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys)