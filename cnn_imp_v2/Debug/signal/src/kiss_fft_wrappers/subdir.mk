################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CC_SRCS += \
../signal/src/kiss_fft_wrappers/kiss_fft_float.cc \
../signal/src/kiss_fft_wrappers/kiss_fft_int16.cc \
../signal/src/kiss_fft_wrappers/kiss_fft_int32.cc 

CC_DEPS += \
./signal/src/kiss_fft_wrappers/kiss_fft_float.d \
./signal/src/kiss_fft_wrappers/kiss_fft_int16.d \
./signal/src/kiss_fft_wrappers/kiss_fft_int32.d 

OBJS += \
./signal/src/kiss_fft_wrappers/kiss_fft_float.o \
./signal/src/kiss_fft_wrappers/kiss_fft_int16.o \
./signal/src/kiss_fft_wrappers/kiss_fft_int32.o 


# Each subdirectory must supply rules for building sources it contributes
signal/src/kiss_fft_wrappers/%.o signal/src/kiss_fft_wrappers/%.su signal/src/kiss_fft_wrappers/%.cyclo: ../signal/src/kiss_fft_wrappers/%.cc signal/src/kiss_fft_wrappers/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m7 -std=gnu++14 -g3 -DDEBUG -DARM_MATH_CM7 -DARM_MATH_DSP -DCMSIS_NN -DUSE_HAL_DRIVER -DSTM32F746xx -DTF_LITE_STATIC_MEMORY -c -I../Core/Inc -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/AI_Inc" -IDrivers/CMSIS/Include -IDrivers/CMSIS/Device/ST/STM32F7xx/Include -IMiddlewares/Third_Party/CMSIS/NN/Include -IMiddlewares/Third_Party/CMSIS/DSP/Include -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/Core/Inc" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/tensorflow" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/flatbuffers/include" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/gemmlowp" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/kissfft" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/ruy" -O3 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-signal-2f-src-2f-kiss_fft_wrappers

clean-signal-2f-src-2f-kiss_fft_wrappers:
	-$(RM) ./signal/src/kiss_fft_wrappers/kiss_fft_float.cyclo ./signal/src/kiss_fft_wrappers/kiss_fft_float.d ./signal/src/kiss_fft_wrappers/kiss_fft_float.o ./signal/src/kiss_fft_wrappers/kiss_fft_float.su ./signal/src/kiss_fft_wrappers/kiss_fft_int16.cyclo ./signal/src/kiss_fft_wrappers/kiss_fft_int16.d ./signal/src/kiss_fft_wrappers/kiss_fft_int16.o ./signal/src/kiss_fft_wrappers/kiss_fft_int16.su ./signal/src/kiss_fft_wrappers/kiss_fft_int32.cyclo ./signal/src/kiss_fft_wrappers/kiss_fft_int32.d ./signal/src/kiss_fft_wrappers/kiss_fft_int32.o ./signal/src/kiss_fft_wrappers/kiss_fft_int32.su

.PHONY: clean-signal-2f-src-2f-kiss_fft_wrappers

