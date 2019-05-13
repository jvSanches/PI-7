/*
 * Modulo: Programa Trajetoria
 * Armazena o programa da trajetoria a ser executada
 */

// max NC program size
#define MAX_PROGRAM_LINES 50

#include "programa_trajetoria.h"

// structure to store NC program
ptj_Data ptj_program[MAX_PROGRAM_LINES];

void ptj_storeProgram(char* texto) {
	// IMPLEMENTAR!!
}// ptj_storeProgram

ptj_Data ptj_getLine(int line) {
	return ptj_program[line];
} // ptj_getLine

void ptj_init() {
  int i;

  for (i=0; i<MAX_PROGRAM_LINES;i++) {
	  ptj_program[i].x = 0;
	  ptj_program[i].y = 0;
	  ptj_program[i].z = 0;
  }
} //ptj_init
