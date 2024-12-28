import numpy as np
from tensorflow.keras.preprocessing import image # type: ignore
import bentoml, mlflow



class PredictionPipeline:
    def __init__(self,filename):
        self.filename =filename


    
    def predict(self):

        imagename = self.filename
        test_image = image.load_img(imagename, target_size = (224,224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)

        # load model
        try:
            model_uri = mlflow.get_artifact_uri("models/VGG16")
            print(f"model uri: {model_uri}")
            model = mlflow.keras.load_model(model_uri)
            result = np.argmax(model.predict(test_image), axis=1)
        
        except:
            try:
                print("""

    facing error in 1st try catche

    """) 
                model_uri = f"models:/VGG16@latest"
                model = mlflow.keras.load_model(model_uri)
                result = np.argmax(model.predict(test_image), axis=1)

            except:
                print("""

    facing error in 2nd try catche

    """) 
                model = bentoml.keras.get("VGG16:latest").to_runner()
                model.init_local()
                result = np.argmax(model.predict.run(test_image), axis=1)


        print(result)

        if result[0] == 1:
            prediction = 'Healthy'
            return [{ "image" : prediction}]
        else:
            prediction = 'Coccidiosis'
            return [{ "image" : prediction}]
