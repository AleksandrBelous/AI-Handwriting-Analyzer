import tensorflow as tf
from tensorflow.keras import layers, models, callbacks, optimizers, losses, metrics
from sklearn.model_selection import train_test_split
import numpy as np

# Создание модели
modls = []
a, b, c = 8, 12, 4
for i in range(a, b, c):
    model = models.Sequential([
        layers.Dense(i, input_shape=(3,), activation='relu'),
        layers.Dropout(0.5),
        # layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    # Компиляция модели
    model.compile(optimizer=optimizers.SGD(),
                  loss=losses.binary_crossentropy,
                  metrics=[metrics.binary_accuracy])

    early_stop = callbacks.EarlyStopping(monitor='val_accuracy',
                                         patience=5,
                                         restore_best_weights=True,
                                         mode='max',
                                         verbose=1)
    checkpoints = callbacks.ModelCheckpoint(f'best_model_{i}.h5',
                                            monitor='val_accuracy',
                                            save_best_only=True,
                                            mode='max',
                                            verbose=1,)
    # Обучение модели
    model.fit(X_train, y_train,
              epochs=5,
              batch_size=32,
              validation_split=0.3,
              callbacks=[early_stop, checkpoints],
              verbose=True)

    # Оценка модели
    loss, accuracy = model.evaluate(X_test, y_test, verbose=True)
    # print(f"i = {i}: Test Accuracy: {accuracy:.4f}")
    modls.append((accuracy, model))
for i in range(len(modls)):
    print(i, modls[i][0])