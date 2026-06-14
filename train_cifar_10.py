
import os
import random
import numpy as np
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

#reproducibility
seed = 42

random.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)

# Paths
MODEL_DIR = 'models'
KERAS_MODEL_PATH = os.path.join(MODEL_DIR, 'cifar10_cnn.h5')

os.makedirs(MODEL_DIR, exist_ok=True)

# DataSet
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

class_names = ['airplane', 'automobile', 'truck', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship']

y_train = y_train.squeeze().astype(np.int64)
y_test = y_test.squeeze().astype(np.int64)

# Normalize pixel values to [0, 1]
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

print(x_train.shape)
print(x_test.shape)

# Model Architecture
def build_model():
    model = keras.Sequential([
    
    layers.Input(shape=(32, 32, 3)),
    layers.Conv2D(32, (3, 3), padding='same'),
    layers.BatchNormalization(),
    layers.ReLU(),
    layers.Conv2D(32, (3, 3), padding='same'),
    layers.BatchNormalization(),
    layers.ReLU(),
    layers.MaxPooling2D(),

    layers.Conv2D(64, (3, 3), padding='same'),
    layers.BatchNormalization(),
    layers.ReLU(),

    layers.Conv2D(64, (3, 3), padding='same'),
    layers.BatchNormalization(),
    layers.ReLU(),
    layers.MaxPooling2D(),

    layers.Conv2D(128, (3, 3), padding='same'),
    layers.BatchNormalization(),
    layers.ReLU(),

    layers.GlobalAveragePooling2D(),
    layers.Dense(10, activation='softmax')
    ])

    return model

model = build_model()
model.summary()

model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-4),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
# Train the model

callbacks = [
    keras.callbacks.ModelCheckpoint(KERAS_MODEL_PATH, save_best_only=True, monitor='val_loss'),
    keras.callbacks.EarlyStopping(monitor='val_loss', patience=40, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-5,verbose=1)
]

history = model.fit(x_train, y_train, epochs=60, batch_size=64,validation_split=0.2,callbacks=callbacks ,verbose=1)

#evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f'Test accuracy: {test_acc:.4f}')
print(f'Test loss: {test_loss:.4f}')




