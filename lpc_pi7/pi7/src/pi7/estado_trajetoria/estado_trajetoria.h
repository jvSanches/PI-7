#ifndef __estado_trajetoria_h
#define __estado_trajetoria_h

// external interface
extern int stt_getCurrentLine();
extern void stt_setCurrentLine(int line);
extern float stt_getX();
extern float stt_getY();
extern float stt_getZ();
extern void stt_setX(float x);
extern void stt_setY(float y);
extern void stt_setZ(float z);
extern void stt_init();
#endif
