from src.logger import logging
from src.components.model.evaluation import ModelEvaluation


if __name__=="__main__":
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


