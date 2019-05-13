#ifndef __programa_trajetoria_h
#define __programa_trajetoria_h


typedef struct {
	float x;
	float y;
	float z;
} ptj_Data;

extern void ptj_storeProgram(char* texto);
extern ptj_Data ptj_getLine(int line);
extern void ptj_init();
#endif
