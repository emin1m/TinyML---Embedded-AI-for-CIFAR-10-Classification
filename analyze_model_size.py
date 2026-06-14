"""
Keras/H5 ve TFLite model boyutu analizi.

Bu script şunları raporlar:
- Keras model dosya boyutu
- TFLite model dosya boyutu
- Keras model parametre sayısı
- Layer bazlı parametreler
- TFLite input/output tensor bilgileri
- TFLite operator listesi
- Tensor detayları
- STM32 için kaba Flash/RAM yorumu

Kullanım:
    python analyze_model_size.py
"""

import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

import numpy as np
import tensorflow as tf
from tflite_interpreter_utils import create_tflite_interpreter

# ============================================================
# Paths
# ============================================================


# Eğer .h5 kullanıyorsan bunu değiştir:
KERAS_MODEL_PATH = "models/cifar10_cnn.h5"

TFLITE_MODEL_PATH = "models/cifar10_cnn_float32.tflite"

# STM32F746 target notes:
# - Exact Flash size depends on the package/part number, but STM32F746 parts are
#   commonly used with up to 1 MB internal Flash.
# - SRAM is 320 KB total, with 64 KB DTCM for fast data. ITCM and backup SRAM are
#   useful, but they should not be counted as general-purpose tensor arena RAM.
STM32F746_FLASH_BYTES = 1024 * 1024
STM32F746_SRAM_BYTES = 320 * 1024
STM32F746_DTCM_BYTES = 64 * 1024
STM32F746_ITCM_BYTES = 16 * 1024
STM32F746_BACKUP_SRAM_BYTES = 4 * 1024


# ============================================================
# Helpers
# ============================================================

def file_size_bytes(path):
    if not os.path.exists(path):
        return None
    return os.path.getsize(path)


def human_size(num_bytes):
    if num_bytes is None:
        return "file not found"

    units = ["B", "KB", "MB", "GB"]
    size = float(num_bytes)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} TB"


def print_section(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# File size analysis
# ============================================================

print_section("FILE SIZE ANALYSIS")

keras_size = file_size_bytes(KERAS_MODEL_PATH)
tflite_size = file_size_bytes(TFLITE_MODEL_PATH)

print(f"Keras model path : {KERAS_MODEL_PATH}")
print(f"Keras model size : {human_size(keras_size)}")

print(f"TFLite model path: {TFLITE_MODEL_PATH}")
print(f"TFLite model size: {human_size(tflite_size)}")

if keras_size and tflite_size:
    ratio = tflite_size / keras_size
    print(f"TFLite / Keras size ratio: {ratio:.4f}")


# ============================================================
# Keras model analysis
# ============================================================

print_section("KERAS MODEL ANALYSIS")

if os.path.exists(KERAS_MODEL_PATH):
    model = tf.keras.models.load_model(KERAS_MODEL_PATH)

    model.summary()

    total_params = model.count_params()

    trainable_params = int(
        np.sum([np.prod(v.shape) for v in model.trainable_weights])
    )

    non_trainable_params = int(
        np.sum([np.prod(v.shape) for v in model.non_trainable_weights])
    )

    print()
    print("Total params        :", total_params)
    print("Trainable params    :", trainable_params)
    print("Non-trainable params:", non_trainable_params)

    # Float32 ağırlıklar için kaba raw weight size
    raw_weight_bytes_float32 = total_params * 4

    print()
    print("Approx raw weight size if float32:")
    print("  Bytes:", raw_weight_bytes_float32)
    print("  Human:", human_size(raw_weight_bytes_float32))

    print()
    print("Layer-wise parameter count:")

    for layer in model.layers:
        params = layer.count_params()
        print(f"  {layer.name:30s} {layer.__class__.__name__:25s} params={params}")

else:
    print("Keras model file not found.")


# ============================================================
# TFLite interpreter analysis
# ============================================================

print_section("TFLITE INTERPRETER ANALYSIS")

if os.path.exists(TFLITE_MODEL_PATH):
    interpreter = create_tflite_interpreter(model_path=TFLITE_MODEL_PATH)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    tensor_details = interpreter.get_tensor_details()

    print("Input details:")
    for item in input_details:
        print(item)

    print()
    print("Output details:")
    for item in output_details:
        print(item)

    print()
    print("Number of tensors:", len(tensor_details))

    print()
    print("Tensor details:")
    print(f"{'index':>5s} {'name':40s} {'shape':20s} {'dtype':15s} {'bytes':>10s}")

    total_tensor_bytes = 0

    for t in tensor_details:
        shape = t.get("shape", [])
        dtype = t.get("dtype", None)

        if dtype is not None:
            try:
                itemsize = np.dtype(dtype).itemsize
                numel = int(np.prod(shape)) if len(shape) > 0 else 1
                tensor_bytes = numel * itemsize
            except Exception:
                tensor_bytes = 0
        else:
            tensor_bytes = 0

        total_tensor_bytes += tensor_bytes

        print(
            f"{t['index']:5d} "
            f"{t['name'][:40]:40s} "
            f"{str(shape):20s} "
            f"{str(dtype):15s} "
            f"{tensor_bytes:10d}"
        )

    print()
    print("Sum of listed tensor buffer sizes:")
    print("  Bytes:", total_tensor_bytes)
    print("  Human:", human_size(total_tensor_bytes))

else:
    print("TFLite model file not found.")


# ============================================================
# TFLite operator analysis
# ============================================================

print_section("TFLITE OPERATOR ANALYSIS")

if os.path.exists(TFLITE_MODEL_PATH):
    with open(TFLITE_MODEL_PATH, "rb") as f:
        model_content = f.read()

    try:
        analysis = tf.lite.experimental.Analyzer.analyze(
            model_content=model_content
        )
        print(analysis)
    except Exception as e:
        print("TFLite Analyzer failed.")
        print("Reason:", e)
else:
    print("TFLite model file not found.")


# ============================================================
# STM32 rough memory notes
# ============================================================

print_section("STM32 ROUGH MEMORY NOTES")

print("Target MCU: STM32F746")
print(f"  Internal Flash assumption : {human_size(STM32F746_FLASH_BYTES)}")
print(f"  Total SRAM assumption     : {human_size(STM32F746_SRAM_BYTES)}")
print(f"  DTCM RAM                  : {human_size(STM32F746_DTCM_BYTES)}")
print(f"  ITCM RAM                  : {human_size(STM32F746_ITCM_BYTES)}")
print(f"  Backup SRAM               : {human_size(STM32F746_BACKUP_SRAM_BYTES)}")

if tflite_size:
    print("Model weights/storage:")
    print(f"  TFLite model stored in Flash approximately: {human_size(tflite_size)}")
    print(f"  Flash usage by model only: {100 * tflite_size / STM32F746_FLASH_BYTES:.2f}%")
    print("  Comment: Flash looks acceptable for STM32F746, but firmware,")
    print("  TensorFlow Lite Micro kernels, startup code, and application code")
    print("  must also fit in the same Flash budget.")

print()
print("CIFAR-10 input buffer:")
input_float32_bytes = 1 * 32 * 32 * 3 * 4
input_uint8_bytes = 1 * 32 * 32 * 3 * 1

print(f"  Float32 input: {input_float32_bytes} bytes = {human_size(input_float32_bytes)}")
print(f"  Uint8/int8 input: {input_uint8_bytes} bytes = {human_size(input_uint8_bytes)}")

print()
print("Output buffer:")
output_float32_bytes = 10 * 4
output_int8_bytes = 10 * 1

print(f"  Float32 output: {output_float32_bytes} bytes = {human_size(output_float32_bytes)}")
print(f"  Int8 output: {output_int8_bytes} bytes = {human_size(output_int8_bytes)}")

print()
print("STM32F746 RAM interpretation:")
if "total_tensor_bytes" in globals():
    print(f"  PC-listed tensor buffers: {human_size(total_tensor_bytes)}")
    print(f"  Share of total SRAM     : {100 * total_tensor_bytes / STM32F746_SRAM_BYTES:.2f}%")
    print(f"  Share of DTCM only      : {100 * total_tensor_bytes / STM32F746_DTCM_BYTES:.2f}%")

    estimated_arena_low = int(total_tensor_bytes * 1.10)
    estimated_arena_high = int(total_tensor_bytes * 1.50)

    print("  Rough tensor arena range:")
    print(f"    Low  estimate: {human_size(estimated_arena_low)}")
    print(f"    High estimate: {human_size(estimated_arena_high)}")

    if estimated_arena_high > STM32F746_SRAM_BYTES:
        print("  Comment: Float32 deployment is likely too large for internal SRAM")
        print("  once stack, heap, DMA buffers, and runtime overhead are included.")
    elif estimated_arena_high > int(STM32F746_SRAM_BYTES * 0.70):
        print("  Comment: Float32 deployment may fit, but RAM margin is tight.")
        print("  Expect linker placement and tensor_arena tuning to matter.")
    else:
        print("  Comment: Float32 deployment has a plausible internal-SRAM path,")
        print("  but the real TFLite Micro arena must still be measured on target.")

    if total_tensor_bytes > STM32F746_DTCM_BYTES:
        print("  DTCM note: The whole arena cannot fit in 64 KB DTCM.")
        print("  Keep only latency-critical buffers/stack in DTCM if needed.")

print()
print("Recommendation for STM32F746:")
print("  1. Prefer full int8 quantization for the STM32 target.")
print("  2. Keep the input as uint8/int8 if your capture pipeline allows it.")
print("  3. Use float32 mainly as a correctness baseline on PC.")
print("  4. Measure the real tensor_arena size with AllocateTensors() on STM32F746.")
print("  5. If using camera/LCD/Ethernet/SDRAM, reserve RAM for DMA-aligned buffers.")

print()
print("Important:")
print("  The TFLite file size mostly affects Flash.")
print("  Tensor arena size affects RAM.")
print("  Exact tensor arena requirement is best found on STM32 by trying AllocateTensors().")
print("  PC tensor byte sum is only an approximation; TFLite Micro arena usage can differ.")
