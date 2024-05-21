from tensorflow.keras.models import load_model
from numpy import array


class NN:
    def __init__(self):
        self.model = load_model('./models/_0.993771.h5')

    def get_prediction(self, request: list):
        return round(self.model.predict(array(request).reshape(1, 3), verbose=False)[0][0])
