################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CC_SRCS += \
../signal/micro/kernels/delay.cc \
../signal/micro/kernels/energy.cc \
../signal/micro/kernels/fft_auto_scale.cc \
../signal/micro/kernels/filter_bank.cc \
../signal/micro/kernels/filter_bank_log.cc \
../signal/micro/kernels/filter_bank_spectral_subtraction.cc \
../signal/micro/kernels/filter_bank_square_root.cc \
../signal/micro/kernels/framer.cc \
../signal/micro/kernels/irfft.cc \
../signal/micro/kernels/overlap_add.cc \
../signal/micro/kernels/pcan.cc \
../signal/micro/kernels/rfft.cc \
../signal/micro/kernels/stacker.cc \
../signal/micro/kernels/window.cc 

CC_DEPS += \
./signal/micro/kernels/delay.d \
./signal/micro/kernels/energy.d \
./signal/micro/kernels/fft_auto_scale.d \
./signal/micro/kernels/filter_bank.d \
./signal/micro/kernels/filter_bank_log.d \
./signal/micro/kernels/filter_bank_spectral_subtraction.d \
./signal/micro/kernels/filter_bank_square_root.d \
./signal/micro/kernels/framer.d \
./signal/micro/kernels/irfft.d \
./signal/micro/kernels/overlap_add.d \
./signal/micro/kernels/pcan.d \
./signal/micro/kernels/rfft.d \
./signal/micro/kernels/stacker.d \
./signal/micro/kernels/window.d 

OBJS += \
./signal/micro/kernels/delay.o \
./signal/micro/kernels/energy.o \
./signal/micro/kernels/fft_auto_scale.o \
./signal/micro/kernels/filter_bank.o \
./signal/micro/kernels/filter_bank_log.o \
./signal/micro/kernels/filter_bank_spectral_subtraction.o \
./signal/micro/kernels/filter_bank_square_root.o \
./signal/micro/kernels/framer.o \
./signal/micro/kernels/irfft.o \
./signal/micro/kernels/overlap_add.o \
./signal/micro/kernels/pcan.o \
./signal/micro/kernels/rfft.o \
./signal/micro/kernels/stacker.o \
./signal/micro/kernels/window.o 


# Each subdirectory must supply rules for building sources it contributes
signal/micro/kernels/%.o signal/micro/kernels/%.su signal/micro/kernels/%.cyclo: ../signal/micro/kernels/%.cc signal/micro/kernels/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m7 -std=gnu++14 -g3 -DDEBUG -DARM_MATH_CM7 -DARM_MATH_DSP -DCMSIS_NN -DUSE_HAL_DRIVER -DSTM32F746xx -DTF_LITE_STATIC_MEMORY -c -I../Core/Inc -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/AI_Inc" -IDrivers/CMSIS/Include -IDrivers/CMSIS/Device/ST/STM32F7xx/Include -IMiddlewares/Third_Party/CMSIS/NN/Include -IMiddlewares/Third_Party/CMSIS/DSP/Include -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/Core/Inc" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/tensorflow" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/flatbuffers/include" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/gemmlowp" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/kissfft" -I"C:/Users/USER/STM32CubeIDE/workspace_1.15.0/cnn_imp_v2/third_party/ruy" -O3 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-signal-2f-micro-2f-kernels

clean-signal-2f-micro-2f-kernels:
	-$(RM) ./signal/micro/kernels/delay.cyclo ./signal/micro/kernels/delay.d ./signal/micro/kernels/delay.o ./signal/micro/kernels/delay.su ./signal/micro/kernels/energy.cyclo ./signal/micro/kernels/energy.d ./signal/micro/kernels/energy.o ./signal/micro/kernels/energy.su ./signal/micro/kernels/fft_auto_scale.cyclo ./signal/micro/kernels/fft_auto_scale.d ./signal/micro/kernels/fft_auto_scale.o ./signal/micro/kernels/fft_auto_scale.su ./signal/micro/kernels/filter_bank.cyclo ./signal/micro/kernels/filter_bank.d ./signal/micro/kernels/filter_bank.o ./signal/micro/kernels/filter_bank.su ./signal/micro/kernels/filter_bank_log.cyclo ./signal/micro/kernels/filter_bank_log.d ./signal/micro/kernels/filter_bank_log.o ./signal/micro/kernels/filter_bank_log.su ./signal/micro/kernels/filter_bank_spectral_subtraction.cyclo ./signal/micro/kernels/filter_bank_spectral_subtraction.d ./signal/micro/kernels/filter_bank_spectral_subtraction.o ./signal/micro/kernels/filter_bank_spectral_subtraction.su ./signal/micro/kernels/filter_bank_square_root.cyclo ./signal/micro/kernels/filter_bank_square_root.d ./signal/micro/kernels/filter_bank_square_root.o ./signal/micro/kernels/filter_bank_square_root.su ./signal/micro/kernels/framer.cyclo ./signal/micro/kernels/framer.d ./signal/micro/kernels/framer.o ./signal/micro/kernels/framer.su ./signal/micro/kernels/irfft.cyclo ./signal/micro/kernels/irfft.d ./signal/micro/kernels/irfft.o ./signal/micro/kernels/irfft.su ./signal/micro/kernels/overlap_add.cyclo ./signal/micro/kernels/overlap_add.d ./signal/micro/kernels/overlap_add.o ./signal/micro/kernels/overlap_add.su ./signal/micro/kernels/pcan.cyclo ./signal/micro/kernels/pcan.d ./signal/micro/kernels/pcan.o ./signal/micro/kernels/pcan.su ./signal/micro/kernels/rfft.cyclo ./signal/micro/kernels/rfft.d ./signal/micro/kernels/rfft.o ./signal/micro/kernels/rfft.su ./signal/micro/kernels/stacker.cyclo ./signal/micro/kernels/stacker.d ./signal/micro/kernels/stacker.o ./signal/micro/kernels/stacker.su ./signal/micro/kernels/window.cyclo ./signal/micro/kernels/window.d ./signal/micro/kernels/window.o ./signal/micro/kernels/window.su

.PHONY: clean-signal-2f-micro-2f-kernels

