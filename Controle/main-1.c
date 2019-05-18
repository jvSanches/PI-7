///
/*
 * File:   main.c
 * Author: Joao Sanches e Lucas Eder
 * Teste do controlador P, pi7
 * 
 */

// Gerado automaticamento por "Window > PIC Memory Views > Configuration Bits"
// A partir daqui --------------->
#include <xc.h>

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

// CONFIG1
#pragma config FOSC = EC        // Oscillator Selection bits (EC: I/O function 
#pragma config WDTE = OFF       // Watchdog Timer Enable bit (WDT disabled and 
#pragma config PWRTE = OFF      // Power-up Timer Enable bit (PWRT disabled)
#pragma config MCLRE = ON       // RE3/MCLR pin function select bit (RE3/MCLR 
#pragma config CP = OFF         // Code Protection bit (Program memory code pro
#pragma config CPD = OFF        // Data Code Protection bit (Data memory code p
#pragma config BOREN =OFF       // Brown Out Reset Selection bits (BOR disabled)
#pragma config IESO = ON        // Internal External Switchover bit (Internal/E
#pragma config FCMEN = ON       // Fail-Safe Clock Monitor Enabled bit (Fail-Sa
#pragma config LVP = OFF        // Low Voltage Programming Enable bit (RB3 pin 

// CONFIG2
#pragma config BOR4V = BOR21V   // Brown-out Reset Selection bit (Brown-out Res
#pragma config WRT = OFF        // Flash Program Memory Self Write Enable bits 
// <--------------- Até aqui

// Includes do projeto
#include <stdio.h>
#include "always.h"
#include "delay.h"
#include "pwm.h"
#include "serial.h"
#include "string.h"
// Definições

# define a1 PORTBbits.RB3      //Bit para leitura do canal a do encoder esquerdo
# define b1 PORTBbits.RB4      //Bit para leitura do canal b do encoder esquerdo

// Timer 0
#define TMR0_PRESCALER 7                     ///< divide por 256
#define POLLING_PERIOD 196                   ///< 10 ms
#define TMR0_SETTING (0xff - POLLING_PERIOD) ///< valor inicial da contagem d

#define TMR1_POLLING_PERIOD 6250;

// Saídas
#define LED RB5                              ///< bit de saída para o LED
#define BUZZER RB7                           ///< bit para buzzer

//COntrolador 
#define Kp  26//pwm 8 bits 26.44

// variáveis globais vão aqui se existirem
// todas as variáveis globais usadas em interrupção precisam ser "volatile"
volatile char portB;

int constrain(int value, int lLimit, int uLimit){
    if (value > uLimit){
        return(uLimit);
    }else if (value < lLimit){
        return(lLimit);
    }else{
        return(value);
    }
}

void interrupt isr(void) {      // Rotina geral de tratamento de interrupção
  // variáveis locais declaradas static mantém o valor
  static int tick;              // contador de vezes que o Timer 0 interrompe
  
  // Timer 0
  // Interrompe a cada 10 ms aproximadamente.
  // Controla o tempo de debounce da chave em conjunto com o I-O-C do PORT B
  if (T0IE && T0IF) {    // se for interrupção do Timer 0
    //leitura dos encoders a cada 10 ms
    
    TMR0 = TMR0_SETTING;       // recarrega contagem no Timer 0
    T0IF = 0;                  // limpa interrupção
  } // fim - tratamento do Timer 0
  
  
  if (RBIE && RBIF) { // se for mudança estado do Port B
    portB = PORTB; // faz a leitura do Port B, isso reseta a condição de i
    char sVar[30]; 
    sprintf(sVar, "a1 = %d, b1 = %d - ", a1, b1);
    putst(sVar);
    RBIF = 0;           // reseta o flag de interrupção para poder receber outr
  } // fim - tratamento I-O-C PORT B
    //Interrupção do Controlador
  if (TMR1IE && TMR1IF) {  
    
    TMR1 = 0xffff - TMR1_POLLING_PERIOD; // recarrega a constante do Timer 1
    TMR1IF = 0;  // limpa o flag de interrupção
    if (++tick >= 10) { // 
      tick = 0;          // então zera o contador
      LED = ~LED;        // inverte LED  
      
    }
    
  } // fim - Interrupcão do Timer 1
  
  
  // Outras interrupções aqui
  
} // fim - Tratamento de todas as interruções

/// Programa Principal



void main (void) {
  
  // variáveis locais

    //
  // configurações dos periféricos  
  // Timer 0
  // o Timer 0 é utilizado para interrupção periódica a cada 1 ms aproximadamen
  OPTION_REGbits.T0CS = 0; // usa clock interno FOSC/4
  OPTION_REGbits.PSA = 0;  // Prescaler é para Timer 0 e não para WDT
  OPTION_REGbits.PS = TMR0_PRESCALER;  // ajusta Prescaler do Timer 0
  
  //Timer 1
  // Atuação do controlador
  T1CONbits.TMR1CS=0;       //fonte de clock interna
  T1CONbits.T1CKPS=3;        // prescaler 1:8
  T1CONbits.TMR1ON=1;
  TMR1 = 0xffff - TMR1_POLLING_PERIOD;
  
  
  // Port B
  TRISB5 = 0;  // RB5 é saída para LED
  ANS13 = 0;   // RB5/AN13 é digital
  TRISB7 = 0;  // RB7 é saída para BUZZER
  TRISB1 = 1;  //Entradas
  TRISB2 = 1;
  TRISB3 = 1;
  TRISB4 = 1;
  ANS10 = 0; //Digitais
  ANS9 = 0;
  ANS8 = 0;
  ANS11 = 0;
  IOCB=0b00011000;
  
  // Controle de interrupções
  T0IE = 1;   // habilita interrupção do Timer 0
  TMR1IE = 1; // interrupção para Timer 1
  PEIE = 1;   // habilita interrupções de periféricos para poder usar Timer 1
  RBIE =1 ;
  GIE = 1;    // habilita todas as interrupções

  //
  // Inicializações
  serial_init();
 
  // Inicializações da placa local
  pwm_init();     // inicializa PWM
  
  //
  // Configurações iniciais
  //    
   
  pwm_set(1, 0);
  pwm_set(2, 0);
  putst("Hora do show, porra");
  while (1) {// loop
      
  } // fim - loop principal
} // fim - main
