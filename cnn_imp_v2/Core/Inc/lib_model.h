#ifndef LIB_MODEL_H_
#define LIB_MODEL_H_

#include <stdint.h>
#include "tensorflow/lite/c/common.h"

#ifdef __cplusplus
extern "C" {
#endif

int8_t LIB_MODEL_Init(const void* tfliteModel,
                      TfLiteTensor** inputTensor,
                      uint8_t* buffer,
                      uint32_t bufferSize);

int8_t LIB_MODEL_Run(TfLiteTensor** outputTensor);

#ifdef __cplusplus
}
#endif

#endif /* LIB_MODEL_H_ */
