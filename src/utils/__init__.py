from src.exception import CustomException
from src.logger import logging
from box import ConfigBox
from pathlib import Path
import yaml
import sys
import os



def read_yaml(file_path:str)-> ConfigBox:
    """Description: Reads yaml file only

    Args:
        file_path (Path): path of .yaml file having content for extraction

    Returns:
        (Path)
        ConfigBox: Content of .yaml file, like key.value 
    """
    try:
        with open(Path(file_path), "rt") as file_obj:
            return ConfigBox(yaml.safe_load(file_obj))
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)


def create_dirs(path:str)-> None:
    """_summary_

    Args:
        path (str): path for directory creation
    """
    try:
        path = Path(path)
        os.makedirs(path, exist_ok=True)
        logging.info(f"path {path} created")
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)
