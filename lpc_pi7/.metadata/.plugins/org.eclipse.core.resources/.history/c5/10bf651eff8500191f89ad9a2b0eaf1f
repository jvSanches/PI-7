#ifndef __comunicacao_pic_h
#define __comunicacao_pic_h

/** struct for communication between TrajectoryControl
 *  and communication to PIC
 */

typedef struct {
	float setPoint1;
	float setPoint2;
	float setPoint3;
} pic_Data;

extern void pic_sendToPIC(pic_Data data);
extern void pic_init();
extern void pic_StopMotors();
#endif
