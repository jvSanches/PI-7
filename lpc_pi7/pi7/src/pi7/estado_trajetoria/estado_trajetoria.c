/*
 * Modulo: Estado Trajetoria
 * Contem as variaveis de estado da trajetoria e de controle da maquina em geral
 */

#include "estado_trajetoria.h"
#include <stdio.h>

int stt_line;
int stt_x = 0;
int stt_y = 0;
int stt_z = 0;
int progLen = 0;

int stt_getCurrentLine() {
	return stt_line;
} // stt_getCurrentLine

void stt_setCurrentLine(int line) {
	stt_line = line;
} // stt_setCurrentLine

void stt_setProgLen(int nValue){
	progLen = nValue;
}
int stt_getProgLen(){
	return progLen;
}

int stt_getX() {
	return stt_x;
} // stt_getX

int stt_getY() {
	return stt_y;
} // stt_getY

int stt_getZ() {
	return stt_z;
} // stt_getZ

void stt_setX(int x) {
	stt_x = x;
} // stt_setX

void stt_setY(int y) {
	stt_y = y;
} // stt_setY

void stt_setZ(int z) {
	stt_z = z;
} // stt_setZ

void stt_init() {
} // stt_init

