/**
 * Modulo: Comunicacao MODBUS (simplificada)
 * Usa a Serial0 para comunicar-se
 */

/*
 * FreeRTOS includes
 */
#include "FreeRTOS.h"
#include "queue.h"
#include <stdio.h>
#include "task.h"

// Drivers for UART, LED and Console(debug)
#include <cr_section_macros.h>
#include <drivers/spi/spi.h>
#include <NXP/crp.h>
#include "LPC17xx.h"
#include "type.h"
#include "drivers/uart/uart.h"
#include "comunicacao_pic.h"

#define TICKS_FACTOR 48.89
//PINS FOR PIC COMUNICATIONS
#define PIC1_ENABLE 9
#define PIC1_DIR 8
#define PIC1_STEP 7
#define PIC2_ENABLE 6
#define PIC2_DIR 0
#define PIC2_STEP 1

void pic_init(){

	LPC_GPIO0->FIODIR |= (1 << PIC1_ENABLE);     //pic1 enable
	LPC_GPIO0->FIOCLR = (1 << PIC1_ENABLE);

	LPC_GPIO0->FIODIR |= (1 << PIC1_DIR);     //pic1 dir
	LPC_GPIO0->FIOCLR = (1 << PIC1_DIR);

	LPC_GPIO0->FIODIR |= (1 << PIC1_STEP);     //pic1 step
	LPC_GPIO0->FIOCLR = (1 << PIC1_STEP);

	LPC_GPIO0->FIODIR |= (1 << PIC2_ENABLE);     //pic2 enable
	LPC_GPIO0->FIOCLR = (1 << PIC2_ENABLE);

	LPC_GPIO0->FIODIR |= (1 << PIC2_DIR);     //pic2 dir
	LPC_GPIO0->FIOCLR = (1 << PIC2_DIR);

	LPC_GPIO0->FIODIR |= (1 << PIC2_STEP);     //pic 2 step
	LPC_GPIO0->FIOCLR = (1 << PIC2_STEP);

} // pic_init

void pic_StopMotors(){
	LPC_GPIO0->FIOCLR = (1 << PIC1_ENABLE);    //Disables pic 1
	LPC_GPIO0->FIOCLR = (1 << PIC2_ENABLE);    //Disables pic 2
}

void pic_ResetMotors(){
	LPC_GPIO0->FIOCLR = (1 << PIC1_ENABLE);    //Disables pic 1
	LPC_GPIO0->FIOCLR = (1 << PIC2_ENABLE);    //Disables pic 2
	vTaskDelay(10);
	LPC_GPIO0->FIOSET = (1 << PIC1_ENABLE);    //Enables pic 1
	LPC_GPIO0->FIOSET = (1 << PIC2_ENABLE);    //Enables pic 2
}

void sendSteps(int xSteps, int ySteps){
	if (xSteps >= 0){
		LPC_GPIO0->FIOSET = (1 << PIC1_DIR);
	}else{
		LPC_GPIO0->FIOCLR = (1 << PIC1_DIR);
		xSteps = - xSteps;
	}
	if (ySteps >=0){
		LPC_GPIO0->FIOSET = (1 << PIC2_DIR);
	}else{
		LPC_GPIO0->FIOCLR = (1 << PIC2_DIR);
		ySteps = - ySteps;
	}
	int i=0;
	int lastState;

	while ((i < xSteps) && (i < ySteps)){
		if (i < xSteps){
			lastState = LPC_GPIO0->FIOPIN;
			LPC_GPIO0->FIOCLR = lastState & (1 << PIC1_STEP);
			LPC_GPIO0->FIOSET = ((~lastState) & (1 << PIC1_STEP));
		}
		if (i < ySteps){
			lastState = LPC_GPIO0->FIOPIN;
			LPC_GPIO0->FIOCLR = lastState & (1 << PIC2_STEP);
			LPC_GPIO0->FIOSET = ((~lastState) & (1 << PIC2_STEP));
		}
		i++;
		vTaskDelay(1);
	}
}


void pic_sendToPIC(pic_Data data) {
	stt_setX(data.setPoint1);
	stt_setY(data.setPoint2);
	stt_setZ(data.setPoint3);


    //test implementation: show values on debug console
	printf("X=%d Y=%d Z=%d\n", data.setPoint1, data.setPoint2, data.setPoint3);
} // pic_sendToPIC

