#ifndef __interpretador_comando_h
#define __interpretador_comando_h

// identification of registers to read
#define REG_X 0
#define REG_Y 1
#define REG_Z 2
#define REG_LINHA 3

// identification of register to write
#define REG_START 0
#define REG_STOP 1
#define REG_RESUME 2
#define REG_SUSPEND 3
#define JOG_X_POSITIVE 4
#define JOG_X_NEGATIVE 5
#define JOG_Y_POSITIVE 6
#define JOG_Y_NEGATIVE 7
#define TOGGLE_Z 8
#define REF 9
#define START_FILE 10

// error
#define CTL_ERR -1

extern int ctl_ReadRegister(int registerToRead);
extern int ctl_WriteRegister(int registerToWrite, int value);
extern int ctl_WriteProgram(uint8_t* programBytes);
extern void ctl_init();

#endif
