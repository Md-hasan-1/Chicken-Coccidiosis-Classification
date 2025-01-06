from src.logger import logging
from src.components.data.ingestion import DataIngestion


if __name__=="__main__":
    STAGE_NAME = "Data Ingestion stage"
    try:
        logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
        data_ingestion = DataIngestion()
        data_ingestion.start()
        logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logging.exception(e)
        raise e
    
