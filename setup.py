from setuptools import find_packages, setup
from typing import List
import csv

REQUIREMENTS_FILE = "requirements.txt"
HYPHEN_E_DOT = "-e ."
def get_requirements()->List[str]:
    """
    This function will return the list of requirements from requirements.txt
    """
    requirements_list = []
    with open(REQUIREMENTS_FILE,"r") as csv_file:
        requirements = csv.reader(csv_file)
        requirements_list = [requirement[0] for requirement in requirements]
        if HYPHEN_E_DOT in requirements_list:
            requirements_list.remove(HYPHEN_E_DOT)
        return requirements_list

setup(
    name="sensor",
    version="0.0.1",
    author="VinodKumarJodu",
    author_email="vinodkumarjodu@gmail.com",
    find_packages=find_packages(include=["config","sensor", "artifact"]),
    install_requires=get_requirements()
)