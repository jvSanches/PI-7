/*
 * Modulo: Interpretador de Comandos
 * Interpreta os comandos recebidos da IHM e processa-os
 */

#define byte uint8_t
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

// Includes for PI7
#include "interpretador_comando.h"
#include "../estado_trajetoria/estado_trajetoria.h"
#include "../controlador_trajetoria/controlador_trajetoria.h"

// communication with TrajectoryController
extern xQueueHandle qControlCommands;

//Defines Aux register for testing
#define REG_AUX_RD 9
int ctl_AUX = 0;
//Write Aux register
void setAUX(int nValue){
	ctl_AUX = nValue;
}
//Reads Aux Register
int getAUX(){
	return ctl_AUX;
}
/************************************************************************
 ctl_ReadRegister
 Le o valor de um registrador
 Parametros de entrada:
    (int) numero do registrador a ser lido
 Retorno:
    (int) valor atual do registrador
*************************************************************************/
int ctl_ReadRegister(int registerToRead) {
   switch (registerToRead) {
      case REG_X:
         return (int)stt_getX();
      case REG_Y:
         return (int)stt_getY();
      case REG_Z:
         return (int)stt_getZ();
      case REG_LINHA:
         return stt_getCurrentLine();
      case REG_AUX_RD:
    	 return getAUX();
   } // switch
   return CTL_ERR;
} // ctl_ReadRegister

/************************************************************************
 ctl_WriteRegister
 Escreve o valor de um registrador. Notar que, quando for um registrador
 de controle (por exzemplo, INICIAR) deve-se processar as acoes relativas
 a este registrador (no exemplo, iniciar o movimento)
 Parametros de entrada:
    (int) numero do registrador a ser escrito
    (int) valor a ser escrito
 Retorno:
    TRUE se escrita foi aceita, FALSE caso contrario.
*************************************************************************/
int ctl_WriteRegister(int registerToWrite, int value) {
  // TO_DO: implementar
  trj_Data command;
  printf("Register %d Value %d\n", registerToWrite, value);
  switch(registerToWrite) {
  case REG_START:
	  printf("start program\n");
	  command.command = CMD_START;
	  xQueueSend(qControlCommands, &command, portMAX_DELAY);
	  break;
  case REG_STOP:
	  printf("Stop program\n");
	  command.command = CMD_STOP;
	  xQueueSend(qControlCommands, &command, portMAX_DELAY);
	  break;
  case REG_RESUME:
	  printf("Resume program\n");
	  command.command = CMD_RESUME;
	  xQueueSend(qControlCommands, &command, portMAX_DELAY);
	  break;
  case REG_SUSPEND:
	  printf("Suspend program\n");
	  command.command = CMD_SUSPEND;
	  xQueueSend(qControlCommands, &command, portMAX_DELAY);
	  break;
  case JOG_X_POSITIVE:
	  command.command = CMD_JOG;
	  command.cDir = 1;
	  command.cValue = value;
	  break;
  case JOG_X_NEGATIVE:
	  command.command = CMD_JOG;
	  command.cDir = 1;
	  command.cValue = -value;
	  break;
  case JOG_Y_POSITIVE:
	  command.command = CMD_JOG;
	  command.cDir = 2;
	  command.cValue = value;
  	  break;
  case JOG_Y_NEGATIVE:
	  command.command = CMD_JOG;
	  command.cDir = 2;
	  command.cValue = -value;
  	  break;
  case REG_AUX_RD:
	  printf("Aux register\n");
	  setAUX(value);
	  break;
  default:
	  printf("unknown register to write\n");
	  break;
  } //switch
  return TRUE;
} // ctl_WriteRegister

/************************************************************************
 ctl_WriteProgram
 Escreve um programa. Notar que o programa foi informado como um byte[]
 logo compete neste caso ao controlador decodificar o programa e armazena-lo
 no DEVICE_MEMORY.
 Parametros de entrada:
    (byte[]) bytes que compoe o programa de movimentacao
 Retorno:
    TRUE se escrita foi aceita, FALSE caso contrario.
*************************************************************************/
int ctl_WriteProgram(byte* program_bytes) {
  // TO_DO: implementar
  return TRUE;
} // ctl_WriteRegister


void ctl_init(){
} // ctl_init

