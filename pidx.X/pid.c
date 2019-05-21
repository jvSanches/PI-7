//#include "htc.h"
#include <xc.h>
#include "always.h"
#include "serial.h"
#include "stdio.h"

#include "pid.h"
#include "motor.h"
#include "position_sensor.h"

// debug
unsigned char printBuffer[10];

static _EXCITATION excitation;

static _PID_MATH currentPosition;
static _PID_MATH setPoint;
static _PID_MATH integralError;
static _PID_MATH previousError;
static _PID_MATH kProportional;
static _PID_MATH kIntegral;
static _PID_MATH kDerivative;

_EXCITATION pid_scaleExcitation ( _PID_MATH activation) {
   
   excitation = ( _EXCITATION ) activation;
   if (excitation > 0)
     excitation = 150 + excitation;
   else if (excitation < 0)
     excitation = -150 + excitation;
   if (excitation > MAX_EXCITATION)
     excitation = MAX_EXCITATION;
   if (excitation < MIN_EXCITATION)
     excitation = MIN_EXCITATION;
   return excitation;   
} // scaleExcitation


static   _PID_MATH activation;
static   _PID_MATH error;
static   _EXCITATION excitation;

void pid_pid() {

    if (RC5 == 0)
      RC5 = 1;
    else
      RC5 = 0;
   
   currentPosition = pos_getCurrentPosition();
   error = setPoint - currentPosition/5;
   activation = kProportional * error;


   excitation = pid_scaleExcitation(activation);
   GIE = 0;
   mot_setExcitation(excitation);
   GIE = 1;
   if (RC5 == 0)
     RC5 = 1;
   else
     RC5 = 0;

} // pid_pid

void pid_setPoint(_PID_MATH position) {
   setPoint = position;
} // pid_setPoint

void pid_setDerivativeGain(_PID_MATH gain) {
  kDerivative = gain;
} // pid_setDerivativeGain

void pid_setIntegralGain(_PID_MATH gain) {
  kIntegral = gain;
} // pid_setIntegralGain

void pid_setProportionalGain(_PID_MATH gain) {
  kProportional = gain;
} // pid_setProportionalGain

void pid_clearError() {
  integralError = 0.0;
  previousError = 0.0;
} // pid_clearError

void pid_init() {
   integralError = 0.0;
   previousError = 0.0;
   currentPosition = 0;
   kProportional = 1.0;
   kDerivative = 0.0;
   kIntegral = 0.0;
} // pid_init
