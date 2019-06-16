#ifndef __estado_trajetoria_h
#define __estado_trajetoria_h

// external interface
extern int stt_getCurrentLine();
extern void stt_setCurrentLine(int line);
extern int stt_getX();
extern int stt_getY();
extern int stt_getZ();
extern void stt_setX(int x);
extern void stt_setY(int y);
extern void stt_setZ(int z);
extern void stt_init();
void stt_setProgLen(int nValue);
int stt_getProgLen();

#endif
