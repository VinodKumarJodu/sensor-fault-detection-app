import os, sys
from sensor.logger import logging
from sensor.exceptions import SensorException
from sensor.data_access.sensor_data import SensorData
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split
import pandas as pd 
from sensor.utils.main_utils import read_yaml_file
from sensor.constants.training_pipeline_constants import SCHEMA_FILE_PATH


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)
    
    def export_data_into_feature_store(self)-> pd.DataFrame:
        try:
            logging.info("Exporting  Data from MongoDB to feature store :: START")
            sensor_data = SensorData()
            dataframe = sensor_data.export_collection_as_dataframe(collection_name=data_ingestion_config.collection_name)
            logging.info("Exporting  Data from MongoDB to feature store :: END")
        except Exception as e:
            raise SensorException(e, sys)

    def split_data_as_train_test(self, dataframe:pd.DataFrame)-> pd.DataFrame:
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    