/* 
 * File:     pwm.h 
 * Author:   Jun Okamoto Jr.
 * Date:     7/02/2016
 * Comments: Gera PWM para acionamento dos motores
 * Revision history: 
 */

#ifndef PWM_H
#define PWM_H

#include <xc.h>

#define DIR1 RA5  // direção do PWM 1
#define DIR2 RA6  // direção do PWM 2

void pwm_init(); ///< inicializa a funcao de PWM com uma determinada frequencia

void pwm_set(int channel, long duty_cycle); ///< define o duty cycle

void pwm_direction(int dir); ///< altera a direção do movimento

#endif