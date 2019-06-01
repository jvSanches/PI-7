/**
 * Name        : main.c
 * Version     :
 * Description : main definition for FreeRTOS application
 */

// PI7 DEFINES
#define CONTROL_Q_SIZE 1 // queue sizes
#define PIC_Q_SIZE 2
#define DEV_Q_SIZE 20

/*
 * FreeRTOS includes
 */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"
#include <stdio.h>

// Drivers for UART, LED and Console(debug)
#include <cr_section_macros.h>
#include <NXP/crp.h>
#include "LPC17xx.h"
#include "type.h"
#include "drivers/uart/uart.h"
#include "drivers/console/basic_io.h"
#include "drivers/ledonboard/leds.h"
#include "drivers/pwm/pwm.h"
#include "drivers/spi/spi.h"

// Header files for PI7
#include "pi7/controlador_trajetoria/controlador_trajetoria.h"
#include "pi7/comunicacao_pic/comunicacao_pic.h"
#include "pi7/comunicacao_pc/modbus.h"
#include "pi7/programa_trajetoria/programa_trajetoria.h"
#include "pi7/interpretador_comando/interpretador_comando.h"
#include "pi7/estado_trajetoria/estado_trajetoria.h"

const portTickType DELAY_1SEC = 1000 / portTICK_RATE_MS;
const portTickType DELAY_500MS = 500 / portTICK_RATE_MS;
const portTickType DELAY_200MS = 200 / portTICK_RATE_MS;
const portTickType DELAY_10MS = 10 / portTICK_RATE_MS;
const portTickType DELAY_1MS = 1 / portTICK_RATE_MS;


#define USERTASK_STACK_SIZE configMINIMAL_STACK_SIZE

void __error__(char *pcFilename, unsigned long ulLine) {
}

/**
 * Communication queues for data transfer between components
 */
xQueueHandle qControlCommands;
xQueueHandle qCommPIC;
xQueueHandle qCommDev;

portTickType lastWakeTime;


void taskController(void *pvParameters) {
   while(1) {
      com_executeCommunication(); //internally, it calls Controller to process events
      //vTaskDelayUntil(&lastWakeTime, DELAY_1MS);
   } //task loop
} // taskController

/**
 * taskNCProcessing: processes NC Program. It receives commands from Controller
 * via queue qControlCommands (start/pause/resume/abort)
 * Runs every 200ms (may generate up to 5 new setpoints per second to interpolate trajectory)
 * Note the use of vTaskDelayUntil instead of vTaskDelay; this will cause system to run every 200ms.
 */

void taskNCProcessing(void *pvParameters) {
	   trj_Data data;
       lastWakeTime = xTaskGetTickCount();
	   while(1) {
		   data.command = NO_CMD;
           xQueueReceive(qControlCommands, &data, 0); //do not wait for command
           if (data.command != NO_CMD) {
        	   trj_processCommand(data);
           }
           trj_generateSetpoint();
		   vTaskDelayUntil(&lastWakeTime, DELAY_200MS);
	   } //task loop
} // taskNCProcessing
/**
 * taskCommPIC: receive setpoints to send to PICs from queue qCommPIC
 * and send them following PIC protocol
 */
void taskCommPIC(void *pvParameters) {
	pic_Data setpoints;
	while(1) {

		 //xQueueReceive(qCommPIC, &setpoints, portMAX_DELAY);
		 setpoints.setPoint1 = 0;
		 setpoints.setPoint2 = 0;
		 setpoints.setPoint3 = 0;

		 pic_sendToPIC(setpoints);
		 vTaskDelay(DELAY_1MS);
    } //task loop
} // taskCommPIC
int readEndStops(){
	int pins = (LPC_GPIO0->FIOPIN);
	return (pins % 0b1111 << 23 );
}

void taskEmergencyController(void *pvParameters){
	while(1){
		if (readEndStops()){
			pic_StopMotors();
			//cQueueReset(qCommPIC);

		}
		vTaskDelay(DELAY_1MS);
	}
}


unsigned int ki = 0;
void taskBlinkLed(void *lpParameters) {
	while(1) {

		if (ki >50){
			ki = 0;
		}
		led2_invert();
		ki++;

		vTaskDelay(DELAY_1SEC);

	} // task loop
} //taskBlinkLed

static void setupHardware(void) {
	// Put hardware configuration and initialisation in here
    /* SystemClockUpdate() updates the SystemFrequency variable */
	// Warning: If you do not initialize the hardware clock, the timings will be inaccurate
	SystemClockUpdate();

	// init onboard led
	led2_init();


    //vPrintStringAndNumber("Hardware setup completed; portTickRateMS=", portTICK_RATE_MS);
	printf("Hardware setup completed.\n");
} // setupHardware


//static void IOS_init(){
//
//}



static void initComponents() {
  // init components
  com_init();
  trj_init();
  pic_init();
  stt_init();
  ptj_init();
  ctl_init();
  //IOs_init();
  PWM_Init(1, 20);
  PWM_Start(1);
  PWM_Set(1, 10);

  // communication between tasks
  qControlCommands = xQueueCreate(CONTROL_Q_SIZE, sizeof(trj_Data));
  qCommPIC = xQueueCreate(PIC_Q_SIZE, sizeof(pic_Data));
  qCommDev = xQueueCreate(DEV_Q_SIZE, sizeof(char));
} // initComponents

/**
 * Program entry point 
 */

// test datd for ReadRegister: read reg 1 (CoordY)
uint8_t msgReadRegister[] = {0x3a, 0x00, 0x00, 0x30, 0x33, 0x00, 0x00, 0x30, 0x31, 0x33, 0x3c, 0x0d, 0x0a};
// test data for WriteRegister: write reg 0 (START NC PROGRAM)
uint8_t msgWriteRegister[] = {0x3a, 0x30, 0x31, 0x30, 0x36, 0x30, 0x30, 0x30, 0x30, 0x30, 0x31, 0x30, 0x30, 0x0d, 0x0a};


int main(void) {


	//MB+ init Console(debug)
	printf("Nao apague esta linha\n");

	// init hardware
	setupHardware();

	// init components
	initComponents(); // init Modbus

	/* 
	 * Start the tasks defined within this file/specific to this demo. 
	 */
	xTaskCreate( taskController, ( signed portCHAR * ) "Controller", USERTASK_STACK_SIZE, NULL, tskIDLE_PRIORITY, NULL );
	xTaskCreate( taskBlinkLed, ( signed portCHAR * ) "BlinkLed", USERTASK_STACK_SIZE, NULL, tskIDLE_PRIORITY, NULL );
	//xTaskCreate( taskNCProcessing, ( signed portCHAR * ) "NCProcessing", USERTASK_STACK_SIZE, NULL, tskIDLE_PRIORITY, NULL );
//	xTaskCreate( taskCommPIC, ( signed portCHAR * ) "CommPIC", USERTASK_STACK_SIZE, NULL, tskIDLE_PRIORITY, NULL );

	//*************** DEBUG FOR ReadRegister
	// insert ReadRegister msg on qCommDev for debug
	/*for (i=0; i<sizeof(msgReadRegister); i++) {
	   ch = msgReadRegister[i];
  	   xQueueSend(qCommDev, &ch, portMAX_DELAY);
	}
	*/

    // ************** DEBUG FOR WriteRegister
	// insert WriteRegister msg on qCommDev for debug
	/*for (i=0; i<sizeof(msgWriteRegister); i++) {
	   ch = msgWriteRegister[i];
  	   xQueueSend(qCommDev, &ch, portMAX_DELAY);
	}
	*/


	/* 
	 * Start the scheduler. 
	 */
	vTaskStartScheduler();

	/* 
	 * Will only get here if there was insufficient memory to create the idle task. 
	 */
	return 1;
} // main
