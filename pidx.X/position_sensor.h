#ifndef POSITION_SENSOR_H
#define POSITION_SENSOR_H

/*
  CONFIGURACAO DOS PINOS INPUT_A e INPUT_B
*/
#include "position_controller.h"

/*
   INTERFACE
*/
#define _POSITION int
extern _POSITION pos_getCurrentPosition();
extern void pos_setCurrentPosition(_POSITION pos);
extern void pos_updatePosition();
extern void pos_init();


#endif