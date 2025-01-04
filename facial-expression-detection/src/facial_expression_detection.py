import vgg_functions as vgg19


class Detector:
    def __init__(self, model):
        self.model_name = model
        match model:
            case "vgg19":
                self.model = vgg19.load_model()
            case "deepface":
                from deepface import DeepFace
                self.model = DeepFace
            case _:
                raise ValueError("Invalid model name")

    def detect(self, image_obj) -> str:
        match self.model_name:
            case "vgg19":
                return self.detect_expression_vgg19(image_obj)
            case "deepface":
                return self.detect_expression_deepface(image_obj)
            case _:
                raise ValueError("Invalid model name")

    def detect_expression_vgg19(self, image_obj):
        logits = vgg19.predict(image_obj, self.model)
        return vgg19.get_expression(logits)

    def detect_expression_deepface(self, image_obj):
        preds = self.model.analyze(image_obj, actions=['emotion'], enforce_detection=False, detector_backend='skip')
        return preds[0]['dominant_emotion']
