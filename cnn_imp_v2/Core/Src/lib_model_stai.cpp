#include "lib_model_stai.hpp"

extern "C"
{
#include "network.h"
}

#include <cstdint>

STAI_NETWORK_CONTEXT_DECLARE(network_context, STAI_NETWORK_CONTEXT_SIZE)

static int8_t input_buffer[StAiModel::InputSize] __attribute__((aligned(4)));
static int8_t output_buffer[StAiModel::OutputSize] __attribute__((aligned(4)));
static uint8_t activations[STAI_NETWORK_ACTIVATIONS_SIZE] __attribute__((aligned(4)));

static stai_ptr input_ptrs[STAI_NETWORK_IN_NUM];
static stai_ptr output_ptrs[STAI_NETWORK_OUT_NUM];
static stai_ptr activation_ptrs[STAI_NETWORK_ACTIVATIONS_NUM];

int8_t StAiModel::Init()
{
    stai_return_code ret;

    ret = stai_network_init(network_context);
    if (ret != STAI_SUCCESS)
    {
        return -1;
    }

    activation_ptrs[0] = reinterpret_cast<stai_ptr>(activations);
    input_ptrs[0]      = reinterpret_cast<stai_ptr>(input_buffer);
    output_ptrs[0]     = reinterpret_cast<stai_ptr>(output_buffer);

    ret = stai_network_set_activations(network_context,
                                       activation_ptrs,
                                       STAI_NETWORK_ACTIVATIONS_NUM);
    if (ret != STAI_SUCCESS)
    {
        return -2;
    }

    ret = stai_network_set_inputs(network_context,
                                  input_ptrs,
                                  STAI_NETWORK_IN_NUM);
    if (ret != STAI_SUCCESS)
    {
        return -3;
    }

    ret = stai_network_set_outputs(network_context,
                                   output_ptrs,
                                   STAI_NETWORK_OUT_NUM);
    if (ret != STAI_SUCCESS)
    {
        return -4;
    }

    input_ptr_ = input_buffer;
    output_ptr_ = output_buffer;

    return 0;
}

int8_t StAiModel::Run()
{
    stai_return_code ret;

    ret = stai_network_run(network_context, STAI_MODE_SYNC);

    if (ret != STAI_SUCCESS)
    {
        return -1;
    }

    return 0;
}

int8_t* StAiModel::Input()
{
    return input_ptr_;
}

int8_t* StAiModel::Output()
{
    return output_ptr_;
}
