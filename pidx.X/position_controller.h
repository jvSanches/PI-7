/* POSITION CONTROLLER
   System-wide defines
*/

#ifndef POSITION_CONTROLLER_H
#define POSITION_CONTROLLER_H

/* 
  USO DOS SINAIS DE ENTRADA E SAIDA DO PIC
*/

#define LED RB5
#define INPUT_A RC3
#define INPUT_B RC4

/* FOR DEBUG */
#define PRINT_BUFFER_SIZE 10
extern unsigned char printBuffer[PRINT_BUFFER_SIZE];
#endif
