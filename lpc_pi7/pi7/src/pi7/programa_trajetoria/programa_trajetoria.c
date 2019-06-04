/*
 * Modulo: Programa Trajetoria
 * Armazena o programa da trajetoria a ser executada
 */

// max NC program size
#define MAX_PROGRAM_LINES 100

#include "programa_trajetoria.h"
#include "../estado_trajetoria/estado_trajetoria.h"

// structure to store NC program
ptj_Data ptj_program[MAX_PROGRAM_LINES];


void ptj_startFile(int nLine){
	ptj_init();
	stt_setCurrentLine( nLine );
	stt_setProgLen(0);
}

void ptj_storeProgram(float nX, float nY, float nZ) {
	stt_setProgLen(stt_getProgLen()+1);
	int line = stt_getCurrentLine();
	ptj_program[line].x = nX/10;
	ptj_program[line].y = nY/10;
	ptj_program[line].z = nZ/10;
	stt_setCurrentLine( line + 1);
	//printf("X = %f Y = %f  Z = %f   |  line = %d \n",ptj_program[line].x,ptj_program[line].y,ptj_program[line].z,line);

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
