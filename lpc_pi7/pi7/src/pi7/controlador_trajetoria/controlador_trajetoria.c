/**
 * Modulo: Controlador de trajetoria (exemplo!!)
 *
 */

/*
 * FreeRTOS includes
 */
#include "FreeRTOS.h"
#include "queue.h"
#include "task.h"

#include <stdio.h>
#include <math.h>

// Header files for PI7
#include "controlador_trajetoria.h"
#include "../programa_trajetoria/programa_trajetoria.h"
#include "../estado_trajetoria/estado_trajetoria.h"
#include "../comunicacao_pic/comunicacao_pic.h"
#include "../../drivers/pwm/pwm.h"

// local variables

#define TRJ_FACTOR 10
int trj_status;
extern xQueueHandle qCommPIC;

void trj_generateSetpoint() {

   int currLine;
   ptj_Data line;
   pic_Data toPic;

   currLine = stt_getCurrentLine();

   //Finaliza a execucao do programa
   if (currLine >= stt_getProgLen()){
	   trj_status = STATUS_NOT_RUNNING;
   }
   if (trj_status != STATUS_RUNNING) {

	   return;
   }

   //printf("CurrLine %d\n", currLine);
   line = ptj_getLine(currLine);
   int AcX = stt_getX();
   int AcY = stt_getY();


   //Calcula distancias entre setpoints e realiza a divisao dos trechos
   float dx = line.x - AcX;
   float dy = line.y - AcY;

   float dist = sqrt(dx*dx + dy*dy);
   int n = dist / TRJ_FACTOR;
   float hx = dx/n;
   float hy = dy/n;



   //Transmite todos os setpoints calculados
   for (int hi = 1; hi < n; hi++){
	  toPic.setPoint1 = AcX + hi * hx;
	  toPic.setPoint2 = AcY + hi * hy;
	  toPic.setPoint3 = line.z;
	  //printf("controlador X=%d Y=%d Z=%d\n", toPic.setPoint1, toPic.setPoint2, toPic.setPoint3);
	  xQueueSend(qCommPIC, &toPic, portMAX_DELAY);
   }
   toPic.setPoint1 = line.x;
   toPic.setPoint2 = line.y;
   toPic.setPoint3 = line.z;
   //printf("controlador X=%d Y=%d Z=%d\n", toPic.setPoint1, toPic.setPoint2, toPic.setPoint3);
   xQueueSend(qCommPIC, &toPic, portMAX_DELAY);

   // Aguarda o fim do movimento atual da maquina
   while (uxQueueMessagesWaiting(qCommPIC));
   vTaskDelay(20);
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

   if ((data.command == CMD_START)||(data.command == CMD_STOP)) {
	   stt_setCurrentLine(0);
   }
   if (data.command == CMD_JOG){
	   pic_Data jog_data;
	   if (data.cDir == 1){
		   jog_data.setPoint1 = stt_getX() + (10 * data.cValue);
		   jog_data.setPoint2 = stt_getY();
		   jog_data.setPoint3 = stt_getZ();
	   }else if(data.cDir == 2){
		   jog_data.setPoint1 = stt_getX();
		   jog_data.setPoint2 = stt_getY() + (10 * data.cValue);
		   jog_data.setPoint3 = stt_getZ();
	   }
	   xQueueSend(qCommPIC, &jog_data, portMAX_DELAY);
   }
   if (data.command == CMD_FILE){
	   ptj_startFile(data.cValue);
   }

   if (data.command == CMD_ZTOGG){
	   penSet(data.cValue);
   }
   if (data.command == CMD_REF){
	   stt_setX(0);
	   stt_setY(0);
	   penSet(1);
   }
} // trj_executeCommand

void trj_init() {
  trj_status = STATUS_NOT_RUNNING;
} // init
