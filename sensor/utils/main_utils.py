import yaml
from sensor.exceptions import SensorException
from sensor.logger import logging
import os, sys
import numpy as np 
import dill


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safeload(yaml_file)
    except Exception as e:
        raise SensorException(e,sys)
