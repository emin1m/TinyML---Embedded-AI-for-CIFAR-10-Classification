#include "lib_model.h"

#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"

#include <new>
#include <stdint.h>

// Global/static değişkenler.
// Interpreter ve resolver fonksiyondan çıkınca yok olmamalı.
static const tflite::Model* model = nullptr;
static tflite::MicroInterpreter* interpreter = nullptr;
static TfLiteTensor* input = nullptr;
static TfLiteTensor* output = nullptr;

// MicroInterpreter için static bellek.
// new/delete kullanmıyoruz; placement-new kullanacağız.
alignas(tflite::MicroInterpreter)
static uint8_t interpreter_buffer[sizeof(tflite::MicroInterpreter)];

int8_t LIB_MODEL_Init(const void* tfliteModel,
                      TfLiteTensor** inputTensor,
                      uint8_t* buffer,
                      uint32_t bufferSize)
{
    // 1. TFLite modelini FlatBuffer olarak oku
    model = tflite::GetModel(tfliteModel);

    if (model == nullptr)
    {
        return -1;
    }

    // 2. Schema version kontrolü
    if (model->version() != TFLITE_SCHEMA_VERSION)
    {
        return -2;
    }

    // 3. Operator resolver
    // Başlangıç için kolay yol: tüm operatorleri ekler.
    // Çalıştıktan sonra Flash azaltmak için MicroMutableOpResolver'a geçeriz.
    static tflite::MicroMutableOpResolver<8> resolver;

    static bool resolver_initialized = false;

    if (!resolver_initialized)
    {
        resolver.AddConv2D();
        resolver.AddMaxPool2D();
        resolver.AddFullyConnected();
        resolver.AddReshape();
        resolver.AddSoftmax();
        resolver.AddQuantize();
        resolver.AddDequantize();
        resolver.AddMean();

        resolver_initialized = true;
    }

    interpreter = new (interpreter_buffer) tflite::MicroInterpreter(
        model,
        resolver,
        buffer,
        bufferSize
    );

    if (interpreter == nullptr)
    {
        return -3;
    }

    // 5. Tensor arena içinde gerekli bellekleri ayır
    TfLiteStatus allocate_status = interpreter->AllocateTensors();

    if (allocate_status != kTfLiteOk)
    {
        return -4;
    }

    // 6. Input tensor pointer'ını al
    input = interpreter->input(0);

    if (input == nullptr)
    {
        return -5;
    }

    // 7. main.cpp tarafındaki input pointer'ını güncelle
    *inputTensor = input;

    return 0;
}

int8_t LIB_MODEL_Run(TfLiteTensor** outputTensor)
{
    if (interpreter == nullptr)
    {
        return -1;
    }

    // 1. Inference çalıştır
    TfLiteStatus invoke_status = interpreter->Invoke();

    if (invoke_status != kTfLiteOk)
    {
        return -2;
    }

    // 2. Output tensor pointer'ını al
    output = interpreter->output(0);

    if (output == nullptr)
    {
        return -3;
    }

    // 3. main.cpp tarafındaki output pointer'ını güncelle
    *outputTensor = output;

    return 0;
}
