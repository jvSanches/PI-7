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
#include <drivers/spi/spi.h>
#include <NXP/crp.h>
#include "LPC17xx.h"
#include "type.h"
#include "drivers/uart/uart.h"
#include "comunicacao_pic.h"

#define TICKS_FACTOR 48.89


void pic_init(){
	spi_init();
} // pic_init

void xSend(int nPos){
	spi_select(1);
	vTaskDelay(1);
	printf("Sent %d and %d\r\n", nPos >> 7, nPos & 0b1111111);
	spi_txrx2(nPos >> 7);
	spi_txrx2(nPos & 0b1111111);
	spi_select(0);
}
void ySend(int nPos){
	spi_select(2);
	spi_txrx2(nPos >> 7);
	spi_txrx2(nPos & 0b1111111);
	spi_select(0);
}

void pic_StopMotors(){
	spi_select(3);
	spi_txrx2(0b1111111);
	spi_txrx2(0b1111111);
	spi_select(0);
}

void pic_sendToPIC(pic_Data data) {
	stt_setX(data.setPoint1);
	stt_setY(data.setPoint2);
	stt_setZ(data.setPoint3);

	xSend(data.setPoint1);
	ySend(TICKS_FACTOR * data.setPoint2);

    //test implementation: show values on debug console
	printf("X=%d Y=%d Z=%d\n", data.setPoint1, data.setPoint2, data.setPoint3);
} // pic_sendToPIC

