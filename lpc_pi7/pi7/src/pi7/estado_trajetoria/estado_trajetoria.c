/*
 * Modulo: Estado Trajetoria
 * Contem as variaveis de estado da trajetoria e de controle da maquina em geral
 */

#include "estado_trajetoria.h"
#include <stdio.h>

int stt_line;
float stt_x = 66;
float stt_y = 67;
float stt_z = 68;

int stt_getCurrentLine() {
	return stt_line;
} // stt_getCurrentLine

void stt_setCurrentLine(int line) {
	stt_line = line;
} // stt_setCurrentLine

float stt_getX() {
	return stt_x;
} // stt_getX

float stt_getY() {
	return stt_y;
} // stt_getY

float stt_getZ() {
	return stt_z;
} // stt_getZ

void stt_setX(float x) {
	stt_x = x;
} // stt_setX

void stt_setY(float y) {
	stt_y = y;
} // stt_setY

void stt_setZ(float z) {
	stt_z = z;
} // stt_setZ

void stt_init() {
} // stt_init

