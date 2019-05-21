/*
  MULTITASKING IMPLEMENTATION
  
  obs.: Nao consegui encontrar uma forma de fazer
  referencias externas a variaveis volatile static.
  Assim, como o multitasking eh atualizado na rotina de interrupcao,
  foi incluida a implementacao diretamente no main.
  Inclui em um arquivo separado para sugerir a modularizacao
  
*/


volatile static int tsk_timeStamp;

#define NUM_TASKS 3
typedef struct {
   Task taskFunction;
   int   scheduleInterval;
   int   lastActivation;
} TaskControlBlock;

static TaskControlBlock tsk_tasks[NUM_TASKS];
static Task tsk_task;
static int tsk_elapsedTime;

void createTask(int taskID, Task t, int scheduleInterval) {
    tsk_tasks[taskID].taskFunction = t;
    tsk_tasks[taskID].scheduleInterval = scheduleInterval;
    tsk_tasks[taskID].lastActivation = 0;
}  // createTask

void executeTasks() {
    unsigned char i;

    for (i=0; i < NUM_TASKS; i++) {
       tsk_elapsedTime = tsk_timeStamp - tsk_tasks[i].lastActivation;
       if (tsk_elapsedTime > tsk_tasks[i].scheduleInterval) {
          tsk_task = tsk_tasks[i].taskFunction;
          tsk_task();
          tsk_tasks[i].lastActivation = tsk_timeStamp;
       }
    } // for each task
} // executeTasks

