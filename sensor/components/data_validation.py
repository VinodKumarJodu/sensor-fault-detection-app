import os, sys
import pandas as pd 
# from distutis import dir_utils
from scipy.stats import ks_2samp
from sensor.logger import logging
from sensor.exceptions import SensorException
from sensor.constants.training_pipeline_constants import  SCHEMA_FILE_PATH
from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig, DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.utils.main_utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    def drop_zero_std_columns(self, dataframe)-> pd.DataFrame:
        try:
            zero_std_cols = []
            for column in dataframe.columns:
                if dataframe[column].std() == 0:
                    zero_std_cols.append(column)
            dataframe = dataframe.drop(zero_std_cols, axis=1)
            return dataframe 
        except Exception as e:
            raise SensorException(e, sys)

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required Number of Columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e, sys)

    def is_numerical_columns_exist(self, dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns
            numerical_column_present = True
            missing_numerical_columns = []
            for num_col in numerical_columns:
                if num_col not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_columns.append(num_col)
            logging.info(f"Missing Numerical Columns: {missing_numerical_columns}")
            return numerical_column_present
        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold:float=0.05)-> bool:
        try:
            dataset_drift_status: bool = False
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    drift_found = False
                else:
                    drift_found = True
                    dataset_drift_status = True
                report.update({column:{"p_value":float(is_same_dist.pvalue),
                                       "drift_status": drift_found}})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            #creating directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            return dataset_drift_status
        except Exception as e:
            raise SensorException(e, sys)


    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #Reading data from train and test file location
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            #Validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} Train Dataframe does not contain all the columns"

            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} Test Dataframe does not contain all the columns"

            # Validate Numerical Columns
            status =self.is_numerical_columns_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} Train Dataframe does not contain all numerical columns"

            status = self.is_numerical_columns_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} Test Dataframe does not contain all numerical columns"

            if len(error_message) > 0:
                raise Exception(error_message)

            #Check for the Data Drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_ingestion_artifact.train_file_path,
                valid_test_file_path = self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data valiation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    


