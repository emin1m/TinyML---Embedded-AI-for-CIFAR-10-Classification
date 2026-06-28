################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../third_party/kissfft/tools/kiss_fftr.c 

C_DEPS += \
./third_party/kissfft/tools/kiss_fftr.d 

OBJS += \
./third_party/kissfft/tools/kiss_fftr.o 


# Each subdirectory must supply rules for building sources it contributes
third_party/kissfft/tools/%.o third_party/kissfft/tools/%.su third_party/kissfft/tools/%.cyclo: ../third_party/kissfft/tools/%.c third_party/kissfft/tools/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DCMSIS_NN -DARM_MATH_CM7 -DARM_MATH_DSP -DUSE_HAL_DRIVER -DSTM32F746xx -DTF_LITE_STATIC_MEMORY -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/Core/Inc" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/tensorflow" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/AI_Inc" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/flatbuffers/include" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/gemmlowp" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/kissfft" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/ruy" -O3 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-third_party-2f-kissfft-2f-tools

clean-third_party-2f-kissfft-2f-tools:
	-$(RM) ./third_party/kissfft/tools/kiss_fftr.cyclo ./third_party/kissfft/tools/kiss_fftr.d ./third_party/kissfft/tools/kiss_fftr.o ./third_party/kissfft/tools/kiss_fftr.su

.PHONY: clean-third_party-2f-kissfft-2f-tools

