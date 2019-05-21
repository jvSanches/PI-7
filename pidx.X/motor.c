//#include "htc.h"
#include <xc.h>
#include "always.h"
#include "motor.h"

#define BIT4 0x10
#define BIT5 0x20

void mot_setExcitation(_EXCITATION excitation) {
  int value;
  if (excitation >= 0) {
     value = excitation & 0x3FC; // 8 MSB bits
     CCPR1L = (value >> 2);
     value = excitation & 0x0003; // 2 LSB bits
     CCP1Y = 0;
     CCP1X = 0;
     CCP1CON |= (value << 4);
     CCPR2L = 0;
     CCP2Y = 0;
     CCP2X = 0;
  } else {
     value = (-excitation) & 0x3FC; // 8 MSB bits
     CCPR2L = (value >> 2);
     value = excitation & 0x0003; // 2 LSB bits
     CCP2Y = 0;
     CCP2X = 0;
     CCP2CON |= (value << 4);
     CCPR1L = 0;
     CCP1Y = 0;
     CCP1X = 0;
  }
} // mot_setExcitation

void mot_init() {
   PR2=249;
   CCPR1L = 0b00000000;
   CCP1CON = 0b00001100; 
   CCPR2L = 0b00000000;
   CCP2CON = 0b00001100; 
   T2CON = 4;
   mot_setExcitation(0);
} //mot_init