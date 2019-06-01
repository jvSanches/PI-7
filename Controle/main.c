///
/*
 * File:   main.c
 * Author: Joao Sanches
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
#include <stdint.h>
#include "always.h"
#include "delay.h"
#include "pwm.h"
#include "serial.h"
//#include "spi.h"
#include "servoController.h"
// Definições

// Timer 0
#define TMR0_PRESCALER 7                     ///< divide por 4
#define POLLING_PERIOD 195                    ///< 10 ms
#define TMR0_SETTING (0xff - POLLING_PERIOD) ///< valor inicial da contagem d

// Saídas
#define LED RB5                              ///< bit de saída para o LED

//Controlador 
//#define Kp  34//pwm 8 bits 26.44
//int Kp = 1000;

/* Valores teróricos calculados para rad/s. Para converter, dividir aqui por 306
Para o KI, multiplicar por 0.01 (tempo do passo de integração)*/

#define KP 4
#define KD 13
#define KI 0


//Logger
#define MAX_SAMPLES 90

//SPI controll

#define CMD_RESET 0
#define SET_POINT 1
#define COM_END 3
#define COM_SP_HI 1
#define COM_SP_LO 2
#define COM_TIMEOUT 3



// variáveis globais vão aqui se existirem
volatile long encoder1_counter;      //Contador de ticks
volatile char state1;                //estado do encoder
volatile char ab1;                   //leitura do encoder
volatile long motor_pos =0;          //Posicao do motor
volatile long set_point =0;          // posicao desejada

volatile signed char pos_log1[MAX_SAMPLES/2 + 1];
volatile signed char pos_log2[MAX_SAMPLES/2 + 1];

volatile int samples =0;
volatile char sampling = 0;
volatile long last_pos;

volatile unsigned int com_time;

int onlyK = 0;

//long constrain
//Restringe um valor entre dois limites
long constrain(long value, long lLimit, long uLimit){
    if (value > uLimit){
        return(uLimit);
    }else if (value < lLimit){
        return(lLimit);
    }else{
        return(value);
    }
}

void PrintSetpoint(){
    char sVar[20];
    sprintf(sVar, "SetPoint: %d \r\n", set_point);
    putst(sVar);
}

//SetMotor
//Define saida do motor segundo o erro]
void SetMotor(){
    
    static int derivative;
    static int last_err;
    long resp;
    int err = set_point - motor_pos;      //calcula o erro
        
    if (onlyK){
        resp = (err) * KP;            //Controle proporcional
    }else{
    
    derivative = (err - last_err);  //Calcula 1/100 da derivada
    last_err = err;
                
    int P_Response  = KP * err;    
    int D_Response = (KD * derivative);
        
    resp = P_Response + D_Response;
    }
    
    resp = constrain(resp, -255,255 );            //Restringe o duty_cycle
    if (resp > 0){
        pwm_set(1, resp );
        pwm_set(2, 0 );
    }else if(resp < 0){
        pwm_set(1, 0 );
        pwm_set(2, -resp );
    }else{
        pwm_set(1, 0 );
        pwm_set(2, 0 );
    }
}

void SetPoint(int new_val){           //Conversão de unidade de entrada p/ ticks
    if (new_val != set_point){
        
        set_point = new_val;
        PrintSetpoint();
    }
}

void resetCounter(){                 //Reinicia o contador do encoder
    encoder1_counter = 0;
    motor_pos = 0;
}

void motor_reset(){
    pwm_set(1, 0);
    pwm_set(2, 0);
    resetCounter();
    SetPoint(0);
}

uint8_t SPIData; 
int nSPIData;
char set_motor_flag =0;
void interrupt isr(void) {      // Rotina geral de tratamento de interrupção
  static int tick;              // contador de vezes que o Timer 0 interrompe
  
  // Timer 0
  // Interrompe a cada 10 ms aproximadamente.
  if (T0IE && T0IF) {    // se for interrupção do Timer 0
      set_motor_flag = 1;
      if (sampling){
          if (samples < MAX_SAMPLES/2){
            pos_log1[samples] = motor_pos-last_pos;
          }else{
              pos_log2[samples-(MAX_SAMPLES/2)] = motor_pos-last_pos;
          }
          last_pos = motor_pos;
        samples++;
      }
      
      
      
     TMR0 = TMR0_SETTING;       // recarrega contagem no Timer 0
     T0IF = 0;                  // limpa interrupção
  } // fim - tratamento do Timer 0
  
  // Interrupt-on-change do PORT B
  if (RBIE && RBIF) { // se for mudança estado do Port B
    char portB = PORTB; // faz a leitura do Port B, isso reseta a condição de interrupt
    
    ab1 = (portB & 0b00011000) >>3;               //Leitura do estado do encoder
    switch(state1) //Atualização do encoder 1
    {
        case 0:                             //Ambos na parte clara
        if(ab1 == 1){                      //giro no sentido positivo
            state1 = 1;                     //atualização do estado
            encoder1_counter--;             //Incremento do contador
        }
        else if(ab1 == 2){                 //giro no sentido negativo
            state1 = 2;                     //atualização do estado
            encoder1_counter++;             //Incremento do contador
        }
        break;
        case 1:                            //b na parte escura, a na clara
        if(ab1 == 0){
            state1 = 0;
            encoder1_counter++;
        }            
        else if (ab1 == 3){
            state1 = 3;
            encoder1_counter--;
        }
        break;
        case 2:                           //Ambos no esccuro
        if(ab1 == 0){
            state1 = 0;
            encoder1_counter--;
        }
        else if(ab1 == 3){
            state1 = 3;
            encoder1_counter++;
        }
        break;
        case 3:                           //a no escuro, b no claro
        if(ab1 == 2){
            state1 = 2;
            encoder1_counter--;
            } 
        else if (ab1 == 1){
            state1 = 1;
            encoder1_counter++;
        }
        break;
        
        }
    motor_pos = -encoder1_counter;
    RBIF = 0;           // reseta o flag de interrupção para poder receber outr
  } // fim - tratamento
  
  // Outras interrupções aqui
} // fim - Tratamento de todas as interruções

void encoders_init(){
    // define estado inicial dos encoders
    //Encoder 1 :
    state1 = (PORTB & 0b00011000) >>3;
    encoder1_counter = 0;
 
}

/*
//Read commands from spi
void read_command(){
    char command;
    char com_state = 0;
    char set_point_hi;
    char set_point_lo;
    if (spiDataReady()){
        com_time = 0;
        com_state = COM_SP_HI;
        while(com_state != COM_END){
            if (com_time > COM_TIMEOUT ){
                com_state = COM_END;
            }else if(spiDataReady() && (com_state == COM_SP_HI)){
                set_point_hi = spiRead() >> 1;
                com_state = COM_SP_LO;
            }else if (spiDataReady() && (com_state == COM_SP_LO)){
                set_point_lo = spiRead() >> 1;
                com_state = COM_END;
                SetPoint((set_point_hi<<7) | (set_point_lo));
            }                    
        }

    }    
}
*/


/// Programa Principal
void main (void) {
  
  // variáveis locais
  char serialIn = 255;          // caracter recebido pelo canal serial

  //
  // configurações dos periféricos  
  // Timer 0
  // o Timer 0 é utilizado para interrupção periódica a cada 1 ms aproximadamen
  OPTION_REGbits.T0CS = 0; // usa clock interno FOSC/4
  OPTION_REGbits.PSA = 0;  // Prescaler é para Timer 0 e não para WDT
  OPTION_REGbits.PS = TMR0_PRESCALER;  // ajusta Prescaler do Timer 0
  
   // Port B
  TRISB5 = 0;  // RB5 é saída para LED
  ANS13 = 0;   // RB5/AN13 é digital
  TRISB7 = 0;  // RB7 é saída para BUZZER
  TRISB1 = 1;  // RBx é saída
  TRISB2 = 1;  //
  TRISB3 = 1;  //
  TRISB4 = 1;  // 
  ANS10 = 0;   // RBx é digital
  ANS9 = 0;    //
  ANS8 = 0;    //
  ANS11 = 0;   //
  LED=1;
  
  // Controle de interrupções
  T0IE = 1;   // habilita interrupção do Timer 0
  TMR1IE = 0; // interrupção para Timer 1
  PEIE = 1;   // habilita interrupções de periféricos para poder usar Timer 1
  GIE = 1;    // habilita todas as interrupções
  IOCB=0b00011000;  //Bits monitorados no PORTB
  RBIE = 1;   //Habilita interrupção na mudança da porta B
  
  //
  // Inicializações
  serial_init();
  //spi_slave_init();
//  spiInit(SPI_SLAVE_SS_EN, SPI_DATA_SAMPLE_MIDDLE, SPI_CLOCK_IDLE_LOW,SPI_IDLE_2_ACTIVE);
 
  // Inicializações da placa local
  pwm_init();     // inicializa PWM
  
  //
  // Configurações iniciais
  //
  
  //Inicializa encoders
  encoders_init();
  int enc1 = -1;
  
  //
  // Loop principal
  //
 
  
  pwm_set(1, 0);
  pwm_set(2, 0);
  int i = 0;
  
  while (1) {  // para sempre
     
      if (!getServoState()){
          motor_reset();
      }else{
          SetPoint(set_point + getServoCommand());
      }
      
      if (set_motor_flag){
          SetMotor();
          set_motor_flag = 0;
      }
      //continue;
      if (sampling && (samples > MAX_SAMPLES)){
              //Espera a realizacao de leituras
            sampling = 0;

            LED=1;
            //Transmissao do log no serial
            char sVar[20];
            samples = 0;
            sprintf(sVar, "Kp: %d -> ", KP);
            putst(sVar);
            while (samples <= MAX_SAMPLES /2){
                sprintf(sVar, "%d ", pos_log1[samples]);
                putst(sVar);
                samples++;
            }
            while (samples < MAX_SAMPLES){
                sprintf(sVar, "%d ", pos_log2[samples - MAX_SAMPLES / 2]);
                putst(sVar);
                samples++;
            }
            sprintf(sVar, "Fim do teste ");
            putst(sVar);
          }
      char serialIn = chkchr();
      if (serialIn == 'u'){
          resetCounter();
          
          last_pos = 0;
          samples = 0;
          sampling = 1;
          SetPoint(100);
          LED=0;
          
      }else if (serialIn == 'w' ){
          SetPoint(set_point + 100);
      }else if (serialIn == 's'){
          SetPoint(set_point - 100);
      }else if (serialIn == ' '){
          motor_reset();
      }else if (serialIn == 'e' ){
          SetPoint(set_point + 50);
      }else if (serialIn == 'd'){
          SetPoint(set_point - 50);
      }else if (serialIn == '0'){
          SetPoint(0);
      }else if (serialIn == 'k'){
          onlyK = 1;
      }else if (serialIn == 'l'){
          onlyK = 0;
      }
      
    } // fim - loop principal
} // fim - main
