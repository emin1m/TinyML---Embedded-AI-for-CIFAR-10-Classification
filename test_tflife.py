import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

import numpy as np
import tensorflow as tf

from tensorflow import keras
from tflite_interpreter_utils import create_tflite_interpreter


MODEL_DIR = "models"
KERAS_MODEL_PATH = os.path.join(MODEL_DIR, "cifar10_cnn.h5")
TFLITE_MODEL_PATH = os.path.join(MODEL_DIR, "cifar10_cnn_int8.tflite")


class_names = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck"
]


def quantize_input(sample, input_detail):
    dtype = input_detail["dtype"]
    if np.issubdtype(dtype, np.floating):
        return sample.astype(dtype)

    scale, zero_point = input_detail["quantization"]
    if scale <= 0:
        raise ValueError("TFLite input tensor has invalid quantization parameters")

    dtype_info = np.iinfo(dtype)
    quantized = np.round(sample / scale + zero_point)
    return np.clip(quantized, dtype_info.min, dtype_info.max).astype(dtype)


def dequantize_output(output, output_detail):
    if np.issubdtype(output.dtype, np.floating):
        return output.astype(np.float32)

    scale, zero_point = output_detail["quantization"]
    if scale <= 0:
        raise ValueError("TFLite output tensor has invalid quantization parameters")

    return (output.astype(np.float32) - zero_point) * scale


# ============================================================
# Load CIFAR-10
# ============================================================

(_, _), (x_test, y_test) = keras.datasets.cifar10.load_data()

y_test = y_test.squeeze().astype(np.int64)
x_test = x_test.astype("float32") / 255.0


# ============================================================
# Load Keras model
# ============================================================

keras_model = keras.models.load_model(KERAS_MODEL_PATH)


# ============================================================
# Load TFLite model
# ============================================================

interpreter = create_tflite_interpreter(TFLITE_MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Input details:")
print(input_details)

print("Output details:")
print(output_details)


# ============================================================
# Compare one sample
# ============================================================

idx = 0

sample = x_test[idx:idx + 1].astype(np.float32)
label = int(y_test[idx])

keras_output = keras_model.predict(sample, verbose=0)[0]

quantized_sample = quantize_input(sample, input_details[0])
interpreter.set_tensor(input_details[0]["index"], quantized_sample)
interpreter.invoke()
tflite_output_raw = interpreter.get_tensor(output_details[0]["index"])[0]
tflite_output = dequantize_output(tflite_output_raw, output_details[0])

keras_pred = int(np.argmax(keras_output))
tflite_pred = int(np.argmax(tflite_output))

print("True label       :", label, class_names[label])
print("Keras pred       :", keras_pred, class_names[keras_pred])
print("TFLite pred      :", tflite_pred, class_names[tflite_pred])
print("Keras output     :", keras_output)
print("TFLite output    :", tflite_output)

abs_diff = np.abs(keras_output - tflite_output)

print("Max abs diff     :", abs_diff.max())
print("Mean abs diff    :", abs_diff.mean())


# ============================================================
# Accuracy comparison on last 1000 samples
# ============================================================

num_samples = 1000
start_index = len(x_test) - num_samples
x_last = x_test[start_index:].astype(np.float32)
y_last = y_test[start_index:]

keras_outputs = keras_model.predict(x_last, verbose=0)
keras_preds = np.argmax(keras_outputs, axis=1)
keras_correct = int(np.sum(keras_preds == y_last))

tflite_correct = 0
tflite_preds = []

for i in range(start_index, len(x_test)):
    sample = x_test[i:i + 1].astype(np.float32)
    label = int(y_test[i])

    quantized_sample = quantize_input(sample, input_details[0])
    interpreter.set_tensor(input_details[0]["index"], quantized_sample)
    interpreter.invoke()
    output_raw = interpreter.get_tensor(output_details[0]["index"])[0]
    output = dequantize_output(output_raw, output_details[0])

    pred = int(np.argmax(output))
    tflite_preds.append(pred)

    if pred == label:
        tflite_correct += 1

tflite_preds = np.array(tflite_preds, dtype=np.int64)
same_predictions = int(np.sum(keras_preds == tflite_preds))

keras_acc = keras_correct / num_samples
tflite_acc = tflite_correct / num_samples
prediction_match_rate = same_predictions / num_samples

print(f"Keras accuracy on last {num_samples} samples : {keras_acc:.4f}")
print(f"TFLite accuracy on last {num_samples} samples: {tflite_acc:.4f}")
print(f"Keras/TFLite prediction match rate           : {prediction_match_rate:.4f}")
