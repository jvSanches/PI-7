/* 
 * File:     pwm.c 
 * Author:   Jun Okamoto Jr.
 * Date:     7/02/2016
 * Comments: Gera PWM para acionamento dos motores.
 *           Esta implementação é só para testes do hardware, as funções
 *           pwm_init e pwm_set deverão ser implementadas na Atividade 6.
 * Revision history: 
 */

#ifndef PWM_C
#define PWM_C

#include <stdio.h>
#include "always.h"
#include "pwm.h"

#define PWM1 RC2  // somente para teste de hw
#define PWM2 RC1  // somente para teste de hw

///
/// Inicializa a função de PWM com uma determinada frequencia
///

void pwm_init(){
//Desabilita pinos de PWM (seta saídas)
    
TRISC1 = 1; // RC1 é configurado como entrada
TRISC2 = 1; // RC2 é configurado como entrada

//Configura Periodo da PWM
PR2 = 0xFF;  //Valor do registrador para freqûencia 19.53kHz (tabela)

//Configura CCPx como modo PWM (CCPxCON)
CCP1CONbits.CCP1M= 12; // PWM mode; P1A, P1C active-high; P1B, P1D active-high
CCP2CONbits.CCP2M= 12; // PWM mode
//Ajusta duty cycle
//0%
CCPR1L = 0;             //Bits mais significativos 
CCP1CONbits.DC1B=0;         // dois bits menos significativos
CCPR2L = 0;             //Bits mais significativos 

//Configura e dispara timer2
    //Limpa flag de interrupcao
    PIR1bits.TMR2IF = 0;
    //Seta pressscaler
    T2CONbits.T2CKPS = 0; // Prescaler = 1
    //Habilita timer2
    T2CONbits.TMR2ON = 1;
//Espera o timer e habilita a saída PWM
    while (!PIR1bits.TMR2IF){}    //espera a interrupção do timer2
  // Saída dos sinais de PWM
    TRISC1 = 0; // RC1 é configurado como saida
    TRISC2 = 0; // RC2 é configurado como saida
  

  
  // Saída dos sinais de direção
  ANS4 = 0;   // RA5 é digital
  TRISA5 = 0; // RA5 é saída
  TRISA6 = 0; // RA6 é saída
  DIR1 = 0;   // direção do motor 1 (RA5)
  DIR2 = 0;   // direção do motor 2 (RA6)
}


///
/// Define o duty cycle da saida PWM
/// @param channel - canal do PWM (1: motor 1; 2: motor 2)
/// @param duty_cycle - porcentagem do duty cycle x 10 (valor de 0 a 1000)
///
void pwm_set(int channel, long duty_cycle){
  // Não implementado para os testes  
  // deverá ser implementado pelos alunos na Atividade 6
    
    if ((duty_cycle >= 0)&&(duty_cycle <=255)){
        if (duty_cycle !=0){
            duty_cycle = 32 + ((223 * duty_cycle/255));
        }
        switch (channel){
            case 1:
                CCPR1L = duty_cycle;             //Bits mais significativos 
                break;
            case 2:
                CCPR2L = duty_cycle;             //Bits mais significativos 
                break;

        }
    }
}

///
/// Altera a direção de movimento
/// @param dir - código de direção
///              0 - para frente (ou qualquer outro valor)
///              1 - para trás
///              2 - gira para a esquerda
///              3 - gira para a direira
///
void pwm_direction(int dir) {
  switch (dir) {
    case 1: // para trás
      DIR1 = 1;
      DIR2 = 1;
      break;
    case 2: // para a esquerda
      DIR1 = 1;
      DIR2 = 0;
      break;
    case 3: // para a direita
      DIR1 = 0;
      DIR2 = 1;
      break;
    default: // para frente
      DIR1 = 0;
      DIR2 = 0;
  } 
}

#endif
