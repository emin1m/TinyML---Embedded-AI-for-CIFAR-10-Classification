import os
import numpy as np
import tensorflow as tf

from tflite_interpreter_utils import create_tflite_interpreter

# ============================================================
# Ayarlar
# ============================================================

TFLITE_MODEL_PATH = "models/cifar10_cnn_int8.tflite"
OUT_HEADER_PATH = "test_image.h"

# CIFAR-10 test setinden hangi image seçilecek?
TEST_INDEX = 0

class_names = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]

# ============================================================
# CIFAR-10 test image al
# ============================================================

(_, _), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

img = x_test[TEST_INDEX]          # shape: (32, 32, 3), dtype uint8
label = int(y_test[TEST_INDEX][0])

print("Selected test index:", TEST_INDEX)
print("True label:", label, class_names[label])
print("Image shape:", img.shape)
print("Image dtype:", img.dtype)
print("Pixel min/max:", img.min(), img.max())

# Model input'u STM32 tarafında uint8 gördüğümüz için raw image kullanacağız.
input_data = img.reshape(1, 32, 32, 3).astype(np.uint8)

# ============================================================
# TFLite inference
# ============================================================

interpreter = create_tflite_interpreter(TFLITE_MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("\nInput details:")
print(input_details)

print("\nOutput details:")
print(output_details)

input_index = input_details[0]["index"]
output_index = output_details[0]["index"]

input_dtype = input_details[0]["dtype"]
input_scale, input_zero_point = input_details[0]["quantization"]

print("\nInput dtype:", input_dtype)
print("Input scale:", input_scale)
print("Input zero point:", input_zero_point)

if input_dtype != np.uint8:
    raise TypeError(
        f"Bu script STM32'de gördüğümüz uint8 input için yazıldı. "
        f"Ama TFLite input dtype = {input_dtype}"
    )

interpreter.set_tensor(input_index, input_data)
interpreter.invoke()

raw_output = interpreter.get_tensor(output_index).reshape(-1)

output_dtype = output_details[0]["dtype"]
output_scale, output_zero_point = output_details[0]["quantization"]

print("\nOutput dtype:", output_dtype)
print("Output scale:", output_scale)
print("Output zero point:", output_zero_point)

if output_dtype in [np.uint8, np.int8]:
    scores = (raw_output.astype(np.float32) - output_zero_point) * output_scale
else:
    scores = raw_output.astype(np.float32)

predicted_class = int(np.argmax(scores))

print("\nRaw output:")
print(raw_output.tolist())

print("\nScores:")
for i, s in enumerate(scores):
    print(f"{i}: {class_names[i]:10s} raw={int(raw_output[i]):3d} score={s:.6f}")

print("\nPython predicted class:", predicted_class, class_names[predicted_class])
print("True class:", label, class_names[label])

# ============================================================
# test_image.h üret
# ============================================================

flat = img.flatten()

with open(OUT_HEADER_PATH, "w", encoding="utf-8") as f:
    f.write("#ifndef TEST_IMAGE_H_\n")
    f.write("#define TEST_IMAGE_H_\n\n")
    f.write("#include <stdint.h>\n\n")
    f.write("#define TEST_IMAGE_SIZE 3072\n")
    f.write(f"#define TEST_IMAGE_LABEL {label}\n")
    f.write(f"#define TEST_IMAGE_PYTHON_PRED {predicted_class}\n\n")

    f.write("static const uint8_t test_image[TEST_IMAGE_SIZE] = {\n")

    for i, val in enumerate(flat):
        f.write(str(int(val)))

        if i != len(flat) - 1:
            f.write(", ")

        if (i + 1) % 16 == 0:
            f.write("\n")

    f.write("\n};\n\n")
    f.write("#endif /* TEST_IMAGE_H_ */\n")

print(f"\nGenerated header: {OUT_HEADER_PATH}")
