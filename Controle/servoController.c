

#include "servoController.h"

#define SERVO_ENABLE RC3
#define SERVO_STEP   RC4
#define SERVO_DIR    RC5


 

void servoInit(){
    
    TRISC3 = INPUT;      // RC3 Servo Enable
    TRISC4 = INPUT;      // RC4 Step
    TRISC5 = INPUT;      // RC5 dir
}  
int getServoState(){
    return SERVO_ENABLE;
}

int getServoCommand(){
    static char lStep;
    if (SERVO_STEP != lStep){
        lStep = !lStep;
        return ((2*SERVO_DIR) - 1);
    }else{
        return 0;
    }
    
}