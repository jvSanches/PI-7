#ifndef __controlador_trajetoria_h
#define __controlador_trajetoria_h

/**
 * Commands for TrajectoryController
 */

#define NO_CMD      0
#define CMD_START   1
#define CMD_SUSPEND 2
#define CMD_RESUME  3
#define CMD_STOP    4
#define CMD_JOG     5
#define CMD_ZTOGG   6
#define CMD_FILE    7
#define CMD_REF     8
// Possible status for TrajectoryController
#define STATUS_RUNNING   0
#define STATUS_NOT_RUNNING 2

// struct for communication between TrajectoryController and Controller
typedef struct {
	int command;
	int cValue;
	int cDir;
} trj_Data;

// external interface
extern void trj_processCommand(trj_Data data);
extern void trj_generateSetpoint();
extern void trj_init();
#endif
