"""
TFLite modelini C++ byte array formatına çevirir.

Input:
    models/cifar10_cnn_int8.tflite

Output:
    generated/model_data.cc
    generated/model_data.h

Kullanım:
    python tflite_to_cpp_array.py
"""

import os


# ============================================================
# Ayarlar
# ============================================================

TFLITE_MODEL_PATH = "models/cifar10_cnn_int8.tflite"
OUT_DIR = "generated"

ARRAY_NAME = "g_cifar10_model"

CC_PATH = os.path.join(OUT_DIR, "model_data.cc")
H_PATH = os.path.join(OUT_DIR, "model_data.h")


# ============================================================
# Kontroller
# ============================================================

if not os.path.exists(TFLITE_MODEL_PATH):
    raise FileNotFoundError(f"TFLite model bulunamadı: {TFLITE_MODEL_PATH}")

os.makedirs(OUT_DIR, exist_ok=True)


# ============================================================
# TFLite binary oku
# ============================================================

with open(TFLITE_MODEL_PATH, "rb") as f:
    model_bytes = f.read()

model_size = len(model_bytes)

print(f"Model path : {TFLITE_MODEL_PATH}")
print(f"Model size : {model_size} bytes")


# ============================================================
# Header dosyası üret
# ============================================================

header_content = f"""#ifndef MODEL_DATA_H_
#define MODEL_DATA_H_

#include <cstdint>
#ifdef __cplusplus

extern const unsigned char {ARRAY_NAME}[];
extern const int {ARRAY_NAME}_len;

#endif  // MODEL_DATA_H_
"""

with open(H_PATH, "w", encoding="utf-8") as f:
    f.write(header_content)


# ============================================================
# C++ source dosyası üret
# ============================================================

lines = []

lines.append('#include "model_data.h"')
lines.append("")
lines.append("// TFLite model binary converted to C++ array.")
lines.append("// This file is auto-generated. Do not edit manually.")
lines.append("")
lines.append(f"const unsigned char {ARRAY_NAME}[] = {{")

# Her satırda 12 byte yaz
BYTES_PER_LINE = 12

for i in range(0, model_size, BYTES_PER_LINE):
    chunk = model_bytes[i:i + BYTES_PER_LINE]
    hex_values = ", ".join(f"0x{byte:02x}" for byte in chunk)
    lines.append(f"  {hex_values},")

lines.append("};")
lines.append("")
lines.append(f"const int {ARRAY_NAME}_len = {model_size};")
lines.append("")

with open(CC_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))


print("Generated files:")
print(f"  {CC_PATH}")
print(f"  {H_PATH}")