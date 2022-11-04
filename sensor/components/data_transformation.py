import os, sys
from sensor.logger import logging
from sensor.exceptions import SensorException
from sensor.entity.config_entity import DataTranformationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from sensor.constants.training_pipeline_constants import TARGET_COLUMN
from sensor.ml.model.estimator import TargetValueMapping
from sensor.utils.main_utils import save_numpy_array_data, save_object

import numpy as np 
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline


class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTranformationConfig):
        """
        :param data_validation_artifact
        :param data_transfroation_config
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Excepption as e:
            raise SensorException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Excepption as e:
            raise SensorException(e,sys)

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            robust_scaler = RobustScaler() 
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            preprocessor = Pipeline(
                steps= [
                        ("Imputer",simple_imputer),
                        ("Robust Scaler",robust_scaler)
                       ]
            )
            return preprocessor
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_transformation(self,)-> DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_csv(self.data_validation_artifact.valid_train_file_path) 
            test_df = DataTransformation.read_csv(self.data_validation_artifact.valid_test_file_path)
            preprocessor = self.get_data_transformer_object()

            #training df
            input_feature_tarin_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())

            # testing df
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())

            preprocessor_object = preprocessor.fit(input_feature_tarin_df)
            transformed_input_feature_train_df = preprocessor_object.transform(input_feature_tarin_df)
            transformed_input_feature_test_df = preprocessor_object.transform(input_feature_test_df)

            smt = SMOTETomek(sampling_strategy="minority")
            input_feature_tarin_final, target_feature_train_final = smt.fit_resample(transformed_input_feature_train_df, target_feature_train_df)
            input_feature_test_final, target_feature_test_final = smt.fit_resample(transformed_input_feature_test_df, target_feature_test_df)
            
            train_arr = np.c_[input_feature_tarin_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]

            # save numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object,)

            # preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )
            logging.info(f"Data Transformation Artifact: {data_transformation_artifact}")

            return data_transformation_artifact
        except Excepption as e:
            raise SensorException(e, sys)
