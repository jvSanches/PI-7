################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/drivers/console/alloc.c \
../src/drivers/console/basic_io.c \
../src/drivers/console/consoleprint.c 

OBJS += \
./src/drivers/console/alloc.o \
./src/drivers/console/basic_io.o \
./src/drivers/console/consoleprint.o 

C_DEPS += \
./src/drivers/console/alloc.d \
./src/drivers/console/basic_io.d \
./src/drivers/console/consoleprint.d 


# Each subdirectory must supply rules for building sources it contributes
src/drivers/console/%.o: ../src/drivers/console/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -D__NEWLIB__ -DNDEBUG -D__CODE_RED -DPACK_STRUCT_END=__attribute\(\(packed\)\) -DGCC_ARMCM3 -I../src -I../FreeRTOS_include -I../FreeRTOS_portable -Os -g -Wall -c -fmessage-length=0 -fno-builtin -ffunction-sections -fdata-sections -mcpu=cortex-m3 -mthumb -D__NEWLIB__ -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


