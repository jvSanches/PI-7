################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/pi7/programa_trajetoria/programa_trajetoria.c 

OBJS += \
./src/pi7/programa_trajetoria/programa_trajetoria.o 

C_DEPS += \
./src/pi7/programa_trajetoria/programa_trajetoria.d 


# Each subdirectory must supply rules for building sources it contributes
src/pi7/programa_trajetoria/%.o: ../src/pi7/programa_trajetoria/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -D__NEWLIB__ -DDEBUG -D__USE_CMSIS -D__CODE_RED -DPACK_STRUCT_END=__attribute\(\(packed\)\) -DGCC_ARMCM3 -I../src -I../FreeRTOS_include -I../FreeRTOS_portable -I../OtherIncludes -Os -g3 -Wall -c -fmessage-length=0 -fno-builtin -ffunction-sections -fdata-sections -msoft-float -DMALLOC_PROVIDED -mcpu=cortex-m3 -mthumb -D__NEWLIB__ -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


