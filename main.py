from src.logger import logging
from src.components.data.ingestion import DataIngestion
from src.components.data.preprocessing import DataPreprocessing
from src.components.model.evaluation import ModelEvaluation


STAGE_NAME = "Data Ingestion stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestion()
   data_ingestion.start()
   logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logging.exception(e)
        raise e




STAGE_NAME = "Data Preprocessing stage"
try: 
   logging.info(f"*******************")
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   prepare_base_model = DataPreprocessing()
   prepare_base_model.start()
   logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logging.exception(e)
        raise e





STAGE_NAME = "Training and Evaluation stage"
try:
   logging.info(f"*******************")
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   model_evalution = ModelEvaluation()
   model_evalution.start()
   logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
        logging.exception(e)
        raise e




