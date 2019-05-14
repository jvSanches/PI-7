################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/drivers/pwm/pwm.c 

OBJS += \
./src/drivers/pwm/pwm.o 

C_DEPS += \
./src/drivers/pwm/pwm.d 


# Each subdirectory must supply rules for building sources it contributes
src/drivers/pwm/%.o: ../src/drivers/pwm/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -D__NEWLIB__ -DNDEBUG -D__CODE_RED -DPACK_STRUCT_END=__attribute\(\(packed\)\) -DGCC_ARMCM3 -I../src -I../FreeRTOS_include -I../FreeRTOS_portable -Os -g -Wall -c -fmessage-length=0 -fno-builtin -ffunction-sections -fdata-sections -mcpu=cortex-m3 -mthumb -D__NEWLIB__ -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


