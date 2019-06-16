#ifndef __programa_trajetoria_h
#define __programa_trajetoria_h


typedef struct {
	int x;
	int y;
	char z;
} ptj_Data;

extern void ptj_startFile(int nLine);
extern void ptj_storeProgram(int nX, int nY, int nZ);
extern ptj_Data ptj_getLine(int line);
extern void ptj_init();
#endif
