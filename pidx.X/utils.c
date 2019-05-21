/* Includes genericos */
//#include <htc.h>
#include <xc.h>
#include <stdio.h>
#include <stdlib.h>
#include "always.h"
#include "delay.h"

/* includes especificos */
#include "utils.h"
#include "protocol.h"
#include "serial.h"

unsigned char ch;
unsigned char buffer[20];

_PID_MATH convertToReal(unsigned char* chars) {
  _PID_MATH value = 0.0;
  _PID_MATH temp = 0.0;
  _PID_MATH potDez = 1.0;
  _PID_MATH signal = 1.0;
  unsigned char decimal = FALSE;
  unsigned char i = 0;


  if (chars[0] == '-') {
     signal = -1.0;
     i = 1;
  }
  for (; i<MAX_LEN; i++) {
    if (chars[i] == 0)
      break;
    if ( (chars[i] < '0') &&
         (chars[i] > '9') &&
         (chars[i] != '.')) {
      break;
    }
    if (chars[i] == '.') {
       potDez = 0.1;
       decimal = TRUE;
    } else {
        temp = (chars[i] & 0x0f);
        if ( decimal != TRUE ) {
          value = (value * 10.0) + temp;
        } else {
          value = value + (temp * potDez);
          potDez = potDez * 0.1;      
        }

    }
  }
  return value * signal;
} // convertToReal

void printReal( _PID_MATH value) {
       sprintf(buffer, "%f", value);
       putst(buffer);
} // printReal