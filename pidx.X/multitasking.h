#ifndef MULTITASKING_H
#define MULTITASKING_H

/* define Task como uma funcao void */
typedef void (*Task)(void);

/* interface publica */
extern void initTasks();
extern void createTask(int taskID, Task t, int scheduleInterval);
extern void executeTasks();

/* interface voltada ao uso pela rotina de interrupcao */
extern void updateTasksTimers();


#endif