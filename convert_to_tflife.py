
import os
import tensorflow as tf
import numpy as np

MODEL_DIR = "models"
KERAS_MODEL_PATH = os.path.join(MODEL_DIR, "cifar10_cnn.h5")
#TFLITE_MODEL_PATH = os.path.join(MODEL_DIR, "cifar10_cnn_float32.tflite")

TFLITE_INT8_MODEL_PATH = os.path.join(MODEL_DIR, "cifar10_cnn_int8.tflite")

print("Loading Keras model...")
model = tf.keras.models.load_model(KERAS_MODEL_PATH)

print("Loading CIFAR-10 data for representative dataset...")
(x_train, y_train),(x_test, y_test) = tf.keras.datasets.cifar10.load_data()

x_train = x_train.astype(np.float32) / 255.0
def representative_dataset():
    for i in range(100):
        sample = x_train[i:i+1]
        yield [sample]

print("Converting to TFLite int8...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

tflite_model = converter.convert()

with open(TFLITE_INT8_MODEL_PATH, "wb") as f:
    f.write(tflite_model)

print("Saved:", TFLITE_INT8_MODEL_PATH)
print("TFLite model size:", len(tflite_model), "bytes")