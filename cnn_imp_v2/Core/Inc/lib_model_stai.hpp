#ifndef LIB_MODEL_STAI_HPP
#define LIB_MODEL_STAI_HPP

#include <cstdint>

class StAiModel
{
public:
    static constexpr int InputSize = 3072;
    static constexpr int OutputSize = 10;

    StAiModel() = default;

    int8_t Init();
    int8_t Run();

    int8_t* Input();
    int8_t* Output();

private:
    int8_t* input_ptr_ = nullptr;
    int8_t* output_ptr_ = nullptr;
};

#endif // LIB_MODEL_STAI_HPP
