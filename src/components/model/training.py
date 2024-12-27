from keras.applications.vgg16 import VGG16 # type: ignore
from keras import layers, models # type: ignore
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import keras
import sys


@dataclass
class ModelTrainer:
    def build_model(self, hp)-> models:
            try:
                base_model = VGG16(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
                base_model.trainable = False  # Freeze base model

                model = models.Sequential([
                    base_model,
                    layers.Flatten(),
                    layers.Dense(hp.Int('units', min_value=128, max_value=512, step=64), activation='relu'),
                    layers.Dropout(hp.Float('dropout', min_value=0.2, max_value=0.5, step=0.1)),
                    layers.Dense(1, activation='sigmoid')  # Adjust for your number of classes
                ])
                
                model.compile(
                    optimizer=keras.optimizers.Adam(learning_rate=hp.Choice('learning_rate', [1e-2, 1e-3, 1e-4])),
                    loss='binary_crossentropy',
                    metrics=['accuracy']
                )
                return model
            except Exception as e:
                logging.error(e)
                raise CustomException(e, sys)

