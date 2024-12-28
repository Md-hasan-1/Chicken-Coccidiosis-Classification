from src.components.data.preprocessing import DataPreprocessingConfig
from src.components.model.training import ModelTrainer
from src.exception import CustomException
from src.config.configuration import ModelEvaluationConfig
from keras.callbacks import EarlyStopping, TensorBoard # type: ignore
from src.utils import create_dirs
from urllib.request import urlparse
from dataclasses import dataclass
from src.logger import logging
from retrying import retry
from pathlib import Path
import mlflow, bentoml
import numpy as np
import keras_tuner
import dagshub
import sys
import os


@dataclass
class ModelEvaluation:

    @retry(stop_max_attempt_number=2, wait_fixed=10000)  # Retries 1 times with 2 seconds delay
    def start(self):
        try:
            mt = ModelTrainer()
            build_model = mt.build_model
            logging.info("Model Evaluation Initiated")
            tuner = keras_tuner.RandomSearch(
            build_model,
            objective='val_loss',
            max_trials=20
            )

            # getting path for train, val and test data
            X_train_path = os.path.join(DataPreprocessingConfig.train_data_dir, "input_data.npy")
            y_train_path = os.path.join(DataPreprocessingConfig.train_data_dir, "labels.npy")
            X_val_path = os.path.join(DataPreprocessingConfig.val_data_dir, "input_data.npy")
            y_val_path = os.path.join(DataPreprocessingConfig.val_data_dir, "labels.npy")
            X_test_path = os.path.join(DataPreprocessingConfig.test_data_dir, "input_data.npy")
            y_test_path = os.path.join(DataPreprocessingConfig.test_data_dir, "labels.npy")

            # loading data from specified path
            X_train = np.load(Path(X_train_path))
            y_train = np.load(Path(y_train_path))
            X_val = np.load(Path(X_val_path))
            y_val = np.load(Path(y_val_path))
            X_test = np.load(Path(X_test_path))
            y_test = np.load(Path(y_test_path))

            create_dirs(ModelEvaluationConfig.tensorboard_dir) # creating tensorboard_dir
            
            early_stoping = EarlyStopping(patience=10, restore_best_weights=True)
            tensorboard = TensorBoard(ModelEvaluationConfig.tensorboard_dir, histogram_freq=1)

            tuner.search(X_train, y_train, 
                        epochs=50,
                        validation_data=(X_val, y_val),
                        callbacks = [early_stoping, tensorboard]
                        )
            
            with mlflow.start_run():
                best_model = tuner.get_best_models()[0]
                test_loss, test_accuracy = best_model.evaluate(X_test, y_test)
                best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
                
                if test_accuracy < 0.6:
                    model = tuner.hypermodel.build(best_hps)
                    history = model.fit(X_train, y_train, epochs=2, validation_split=(X_val, y_val))
                    
                    val_acc_per_epoch = history.history['val_accuracy']
                    best_epoch = val_acc_per_epoch.index(max(val_acc_per_epoch)) + 1

                    best_model.fit(
                        X_train, y_train,
                        epochs=best_epoch,
                        validation_split=(X_val, y_val),
                        callbacks = [early_stoping, tensorboard]
                    )

                    test_loss, test_accuracy = best_model.evaluate(X_test, y_test)
                
                mlflow.log_metric("loss", test_loss)
                mlflow.log_metric("accuracy", test_accuracy)
                mlflow.log_params(best_hps.values)

                infer_signature = mlflow.models.infer_signature(X_train, best_model.predict(X_train))

                # connecting with dagshub repository
                dagshub.init(repo_owner='Md-hasan-1', repo_name='Chicken-Coccidiosis-Classification', mlflow=True)
                
                uri = "https://dagshub.com/Md-hasan-1/Chicken-Coccidiosis-Classification.mlflow"
                mlflow.set_tracking_uri(uri)
                
                tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

                if tracking_url_type_store != "file":
                    mlflow.keras.log_model(best_model, "VGG16",
                                           registered_model_name="VGG16", 
                                           signature=infer_signature
                                    )
                else:
                    mlflow.keras.log_model(best_model, "VGG16", 
                                           signature=infer_signature
                                    )

                # saving model locally
                bentoml.keras.save_model("VGG16", best_model)

            logging.info("Model Evaluation completed")
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
        

if __name__=="__main__":
    obj = ModelEvaluation()
    obj.start()

