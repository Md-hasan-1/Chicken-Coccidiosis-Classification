from src.logger import logging
from src.components.data.preprocessing import DataPreprocessing


if __name__=="__main__":
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
    
