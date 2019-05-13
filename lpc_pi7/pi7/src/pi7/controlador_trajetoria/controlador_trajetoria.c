/**
 * Modulo: Controlador de trajetoria (exemplo!!)
 *
 */

/*
 * FreeRTOS includes
 */
#include "FreeRTOS.h"
#include "queue.h"

#include <stdio.h>

// Header files for PI7
#include "controlador_trajetoria.h"
#include "../programa_trajetoria/programa_trajetoria.h"
#include "../estado_trajetoria/estado_trajetoria.h"
#include "../comunicacao_pic/comunicacao_pic.h"

// local variables
int trj_status;
extern xQueueHandle qCommPIC;

void trj_generateSetpoint() {
   //TODO: implementar

   int currLine;
   ptj_Data line;
   pic_Data toPic;

   if (trj_status != STATUS_RUNNING) {
	   return;
   }

   currLine = stt_getCurrentLine();
   printf("CurrLine %d\n", currLine);
   line = ptj_getLine(currLine);
   toPic.setPoint1 = line.x;
   toPic.setPoint2 = line.y;
   toPic.setPoint3 = line.z;
   xQueueSend(qCommPIC, &toPic, portMAX_DELAY);
   currLine++;
   stt_setCurrentLine(currLine);
} // trj_generateSetpoint

void trj_processCommand(trj_Data data) {

   if ((data.command == CMD_SUSPEND) || (data.command == CMD_STOP)) {
	   trj_status = STATUS_NOT_RUNNING;
   }
   if ((data.command == CMD_START) || (data.command == CMD_RESUME)) {
	   printf("starting trajectory\n");
	   trj_status = STATUS_RUNNING;
   }

   if (data.command == CMD_START) {
	   stt_setCurrentLine(0);
   }
} // trj_executeCommand

void trj_init() {
  trj_status = STATUS_NOT_RUNNING;
} // init
