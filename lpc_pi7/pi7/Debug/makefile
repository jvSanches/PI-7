################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include src/pi7/programa_trajetoria/subdir.mk
-include src/pi7/interpretador_comando/subdir.mk
-include src/pi7/estado_trajetoria/subdir.mk
-include src/pi7/controlador_trajetoria/subdir.mk
-include src/pi7/comunicacao_pic/subdir.mk
-include src/pi7/comunicacao_pc/subdir.mk
-include src/drivers/uart/subdir.mk
-include src/drivers/spi/subdir.mk
-include src/drivers/pwm/subdir.mk
-include src/drivers/ledonboard/subdir.mk
-include src/drivers/console/subdir.mk
-include src/subdir.mk
-include FreeRTOS_src/subdir.mk
-include FreeRTOS_portable/MemMang/subdir.mk
-include FreeRTOS_portable/subdir.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all: pi7.axf

# Tool invocations
pi7.axf: $(OBJS) $(USER_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: MCU Linker'
	arm-none-eabi-gcc -nostdlib -L../Libraries -msoft-float -DMALLOC_PROVIDED -Xlinker -Map="pi7.map" -mcpu=cortex-m3 -mthumb -T "pi7_Debug.ld" -o "pi7.axf" $(OBJS) $(USER_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '
	$(MAKE) --no-print-directory post-build

# Other Targets
clean:
	-$(RM) $(EXECUTABLES)$(OBJS)$(C_DEPS) pi7.axf
	-@echo ' '

post-build:
	-@echo 'Performing post-build steps'
	-arm-none-eabi-size "pi7.axf"; # arm-none-eabi-objcopy -O binary "pi7.axf" "pi7.bin" ; checksum -p LPC1769 -d "pi7.bin";
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY: post-build

-include ../makefile.targets
