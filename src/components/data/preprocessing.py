from src.exception import CustomException
from src.logger import logging
from src.utils import create_dirs
from keras.applications.vgg16 import preprocess_input # type: ignore
from tensorflow.image import resize # type: ignore
from tensorflow.data import Dataset # type: ignore
from src.config.configuration import DataIngestionConfig, DataPreprocessingConfig
from dataclasses import dataclass
import numpy as np
import os
import sys



@dataclass
class DataPreprocessing:
    def resize_and_scale(self, X):
        """Description: resize image(X) in 224X224 for VGG16

        Args:
            X (image_data): input image for model
        """
        try:
            X = resize(X, (224, 224))/255 # resizing and scaling
            return X
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
    

    def start(self, inputs)-> None:
        """Description: transform data for input of VGG16

        Args:
            inputs (dict): should be in form of dictionaries
        
        Note: Format -> {ReadingPath : SavingPath}
        
        "key" is data reading path were data is already present for transformation,
        "value" is saving path were data will be saved after transformation.
        """
        try:
            logging.info("Data Preprocessing initiated")
            create_dirs(DataPreprocessingConfig.dir_path) # creating main directory
            
            for read_path, save_path in inputs.items():

                read_path = os.path.join(read_path)
                save_path = os.path.join(save_path)
                create_dirs(save_path) # creating saving directory where transformed data will be stored

                data = Dataset.load(read_path) # loading data

                data = data.map(lambda X, y: (self.resize_and_scale(X), y)) # resizing and scaling

                data = data.batch(20, drop_remainder=True) # droping incomplete batch

                data = data.map(lambda X, y: (preprocess_input(X), y)) # converting into input format of VGG16

                # extracting image, label
                X = []
                y = []
                for image_data, label_data in data:
                    X.append(image_data.numpy())
                    y.append(label_data.numpy())

                # creating proper numpy array
                X = np.concatenate(X, axis=0) 
                y = np.concatenate(y, axis=0)

                # saving data
                np.save(os.path.join(save_path, "input_data.npy"), X)
                np.save(os.path.join(save_path, "labels.npy"), y)
            
            logging.info("Data Preprocessing completed")
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)


if __name__=="__main__":
    kwarg = {
        DataIngestionConfig.train_data_dir:DataPreprocessingConfig.train_data_dir, 
        DataIngestionConfig.val_data_dir:DataPreprocessingConfig.val_data_dir, 
        DataIngestionConfig.testing_data_dir:DataPreprocessingConfig.test_data_dir
    }
    obj = DataPreprocessing()
    obj.start(inputs=kwarg)

