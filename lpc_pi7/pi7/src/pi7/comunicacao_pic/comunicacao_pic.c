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

// Drivers for UART, LED and Console(debug)
#include <cr_section_macros.h>
#include <NXP/crp.h>
#include "LPC17xx.h"
#include "type.h"
#include "drivers/uart/uart.h"

// Header files for PI7
#include "comunicacao_pic.h"

void pic_sendToPIC(pic_Data data) {

    // test implementation: show values on debug console
	printf("X=%d Y=%d Z=%d\n", data.setPoint1, data.setPoint2, data.setPoint3);
} // pic_sendToPIC

void pic_init(){

} // pic_init
