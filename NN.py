#!/home/nemo/anaconda3/envs/keylog_tf/bin/python
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np


class NN:
    def __init__(self):
        self.train_labels = None
        self.train_sequences = None
        self.model = models.Sequential(
                [
                        # Маскирование нулевых значений во входных данных
                        layers.Masking(mask_value=0.0, input_shape=(None, 1)),
                        # LSTM слой с 64 нейронами
                        layers.LSTM(64),
                        # Выходной слой с сигмоидной активацией для двоичной классификации
                        layers.Dense(1, activation='sigmoid')
                        ]
                )

    def compile_NN(self):
        self.model.compile(optimizer='adam',
                           loss='binary_crossentropy',
                           metrics=['accuracy']
                           )

    def get_random_datasets(self):
        self.train_sequences = [np.random.rand(np.random.randint(1, 10), 1) for _ in range(100)]
        self.train_labels = np.random.randint(2, size=100)

    def teach_NN(self):
        self.model.fit(self.train_sequences, self.train_labels, epochs=10, batch_size=32)

    def get_prediction(self, sequence):
        # new_sequence = np.random.rand(np.random.randint(1, 10), 1)
        prediction = self.model.predict(np.array([sequence]))
        print("Similarity:", prediction[0][0])


if __name__ == '__main__':
    print('OK')
