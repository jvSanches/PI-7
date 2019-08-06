

#include "servoController.h"

#define SERVO_ENABLE RC3
#define SERVO_STEP   RC4
#define SERVO_DIR    RC5


 
static char lStep = 0 ;
void servoInit(){
     
    TRISC3 = INPUT;      // RC3 Servo Enable (SCK)
    TRISC4 = INPUT;      // RC4 Step         (MISO)
    TRISC5 = INPUT;      // RC5 dir          (MOSI))
    lStep = SERVO_STEP;
}  
int getServoState(){
    return SERVO_ENABLE;
}

int getServoCommand(){
   
    if (SERVO_STEP != lStep){
        lStep = !lStep;
        return ((2*SERVO_DIR) - 1);
    }else{
        return 0;
    }
    
}