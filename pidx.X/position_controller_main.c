/* POSITION CONTROLLER
   O controlador de posicao deve fazer 4 tarefas:
   - ler encoder
   - realizar o controle PID
   - receber setpoints pela serial
   - piscar o led de heartbeat

   A ideia da implementacao eh que havera´ uma interrupcao a cada 0,1ms,
   para que o encoder possa ser lido a 10kHz, ja que a frequencia 
   maxima do encoder eh de 300rpm = 5Hz * 1200 pulsos/rotacao = 6kHz.

   As demais tarefas, fora da leitura do encoder, serao realizadas por
   uma multitasking simplificado, com tick de 1ms. 
   Cada uma das tarefas serah acionada em seu tempo correto;
   as tarefas estao criadas no arquivo tasks.c

   HTC significa HiTech C Compiler, que é outro possivel compilador para a familia 16F
   mas não é o default ao usar a versão MPLAB X IDE.
*/

/* TaskId e intervalo para scheduling de cada uma das tarefas */
#define POLLING_PERIOD 52                    // 12kHz 
#define TMR0_SETTING (0xff - POLLING_PERIOD) // valor inicial da contagem do Timer 0



/* Includes genericos */
//HTC #include <htc.h>
#include <xc.h>
#include <stdio.h>
#include <stdlib.h>
#include "always.h"
#include "delay.h"

/* Includes especificos */
#include "position_controller.h"
#include "multitasking.h"
#include "position_sensor.h"
#include "pid.h"
#include "serial.h"
#include "utils.h"

/* Implementatacoes incluidas diretamente neste arquivo */
#include "position_sensor_implementation.h"
#include "multitasking_implementation.h"

/* Configuracao do PIC */
//HTC __CONFIG(WDTDIS & HS & LVPDIS & BORDIS);
//XC
#pragma config FOSC=EC
#pragma config WDTE=OFF
#pragma config LVP=OFF
#pragma config BOREN=OFF
#pragma config PWRTE=OFF
#pragma config MCLRE=ON
#pragma config CP=OFF
#pragma config CPD=OFF
#pragma config IESO=OFF
#pragma config FCMEN=OFF
#pragma config WRT=OFF
#pragma config DEBUG=ON


void initPic() {
  TRISB = 0x00;         // configuranco RB3-0 como saidas para comunic com LCD
						// RB4 e entrada do botao e RB5 saida para piscar o LED
  TRISC = 0b10011000;   //bit 0 (AIN1) = output
						//bit 1 (pwm) = output
						//bit 2 (pwm) = output
						//bit 3 (A do enconder)= input
						//bit 4 (B encoder)= input
						//bit 5  (livre)
						//bit 6 (tx serial) = output 
						//bit 7 (rx serial)= input 						
  TMR0 = TMR0_SETTING;
  OPTION_REG = 0b11000001;  // programa Timer 0 prescaler 1:4
  T0IE = 1;             // habilita interrupção do Timer 0
} // iniciaPic

/*================================================
  INTERRUPCAO
 */

volatile static unsigned char interruptCounter = 0;

// one tick each 1 msec
#define TICK_COUNT 14   

void interrupt isr(void) {

  if (T0IE && T0IF) {          // se for interrupção do Timer 0
    // update encoder
    // coded here instead of within module POSITION_SENSOR
    // to save time (about 10% by avoiding function call)
    pos_inA = 0;
    pos_inB = 0;

    if (INPUT_B == 1)
      pos_inB = 1;
    if (INPUT_A == 1)
      pos_inA = 2;
    pos_currentEncoder = pos_inA + pos_inB;
    pos_currentPosition += encoderStates[pos_previousEncoder][pos_currentEncoder];
    pos_previousEncoder = pos_currentEncoder;

    // update multitasking timer
    interruptCounter++;
    if (interruptCounter > TICK_COUNT) {
      tsk_timeStamp++;
      interruptCounter = 0;
    }

    TMR0 = TMR0_SETTING;       // recarrega contagem no Timer 0
    T0IF = 0;                  // limpa interrupção
  } 
} // interrupt isr



/*================================================
 CONTROLE DO MULTITASKING
 */

void initSys() {
   initPic();
   initTasks();
} // iniciarSistema


/************************
 Main
*/
void main(void) {
   initSys();
   // habilita interrupcoes somente depois de terminar a iniciacao
   GIE = 1;                   
   while(TRUE) {
     executeTasks();
   } // while true
} // main

/***********************************************
  Main to test encoder

#include "motor.h"
#include "position_sensor.h"
#include "protocol.h"
#include "delay.h"
unsigned char printBuffer[10];
static  _POSITION main_position;
void main() {
  
  initPic();
  pro_init();
  pos_init();
  mot_init();
  GIE = 1;                   
  mot_setExcitation(200);
  while (TRUE) {
    main_position = pos_getCurrentPosition();
    sprintf(printBuffer, "%d ", main_position);
    putst(printBuffer);    
  }
}

/************************************************ 
  main to test protocol 
#include "protocol.h"
#include "pid.h"
extern _PID_MATH convertToReal(char* chars);
_MESSAGE msg;
unsigned char idx = 0;
const unsigned char test[12] = "::ap-1.7;\0";
_PID_MATH aReal;
unsigned char chkchr_test() {
  idx++;
  return test[idx];
} // chkchr_test

void main(void) {
  initPic();
  pro_init();
  pro_setMyId('a');
  idx = 0;
  while(TRUE) {
    msg = pro_getMessage();
    aReal = msg.value;
    printReal(aReal);
  }
} // main
*/
