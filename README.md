

# STM32F746G-DISCO CIFAR-10 INT8 Inference Benchmark

This project runs an INT8 CIFAR-10 CNN model on the STM32F746G-DISCO board and compares different embedded inference runtimes.

The main goal is to show that INT8 quantization alone is not enough for fast inference. Runtime and kernel backend selection have a major impact on latency.

## Hardware

* Board: STM32F746G-DISCO
* MCU: STM32F746NG
* CPU: ARM Cortex-M7
* Clock: 216 MHz
* I-Cache / D-Cache: Enabled

## Model Architecture

* Dataset: CIFAR-10
* Input: `1 x 32 x 32 x 3`, INT8
* Output: `1 x 10`, INT8
* Format: TensorFlow Lite INT8

## Runtime Comparison

| Runtime / Configuration                | Optimization | Inference Time |
| -------------------------------------- | -----------: | -------------: |
| TensorFlow Lite Micro, initial build   |        `-O0` |    ~161,000 ms |
| TensorFlow Lite Micro, optimized build |        `-O3` |     ~40,298 ms |
| STAI / X-CUBE-AI, first run            |        `-O3` |        ~381 ms |
| STAI / X-CUBE-AI, 10-run average       |        `-O3` |        ~138 ms |
| ST Edge AI reported benchmark          |            - |      ~132.6 ms |

## Key Result

The STAI / X-CUBE-AI runtime reached approximately **138 ms per inference**, close to the ST Edge AI reported benchmark.

Compared with the optimized TensorFlow Lite Micro implementation:

```text
40,298 ms / 138 ms ≈ 292x faster
```

This shows that the main bottleneck was not the model itself, but the runtime and low-level kernel backend.

## Project Structure

```text
.
├── stm32/                  # STM32CubeIDE project
│   ├── Core/
│   │   ├── Inc/
│   │   └── Src/
│   ├── AI_Inc/
│   └── Lib/
├── train_cifar_10.py
├── convert_to_tflite.py
├── test_tflite.py
└── README.md
```

## Notes

The ST runtime static library is not included in this repository.
Download the generated package from ST Edge AI / X-CUBE-AI and place the runtime library under:

```text
stm32/Lib/
```

Expected file:

```text
libNetworkRuntime1201_CM7_GCC.a
```

## Next Step

The next goal is to implement a custom TensorFlow Lite Micro + CMSIS-NN path and compare it with the STAI / X-CUBE-AI runtime.
