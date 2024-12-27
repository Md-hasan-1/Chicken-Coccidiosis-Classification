from src.utils import read_yaml
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    config = read_yaml("config/config.yaml").data.ingestion
    dir_path = config.dir_path
    source_uri = config.source_uri
    zip_file_path = config.zip_file_path
    raw_data_dir = config.raw_data_dir
    training_data_dir = config.training_data_dir
    testing_data_dir = config.testing_data_dir
    train_data_dir = config.train_data_dir
    val_data_dir = config.val_data_dir


@dataclass
class DataPreprocessingConfig:
    config = read_yaml("config/config.yaml").data.preprocessing
    dir_path = config.dir_path
    train_data_dir = config.train_data_dir
    val_data_dir = config.val_data_dir
    test_data_dir = config.test_data_dir


@dataclass
class ModelEvaluationConfig:
    config = read_yaml("config/config.yaml")
    tensorboard_dir = config.callbacks.tensorboard_dir

