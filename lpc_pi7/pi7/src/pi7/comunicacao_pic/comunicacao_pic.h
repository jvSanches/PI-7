#ifndef __comunicacao_pic_h
#define __comunicacao_pic_h

/** struct for communication between TrajectoryControl
 *  and communication to PIC
 */

typedef struct {
	int setPoint1;
	int setPoint2;
	int setPoint3;
} pic_Data;

extern void pic_sendToPIC(pic_Data data);
extern void pic_init();
extern void pic_StopMotors();
extern void pic_ResetMotors();
extern void pic_sendSteps(int xSteps, int ySteps);
#endif
