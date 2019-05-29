/* 
 * File:     spi.h 
 * Author:   Bruno Alan Miyamoto ou Thiago ?
 * Date:     7/02/2016
 * Comments: Controla interface SPI
 * Revision history:
 *           [jo:160214] código comentado e alguns ajustes 
 */

#ifndef SPI_C
#define	SPI_C

#include "spi.h"
#include "always.h"

#define SS RC0          // SS para SPI
#define DUMMYDATA 0
#define DATA_READY RB0  // Pino de entrada para receber indicação de que há um byte para ser lido por SPI

///
/// inicializa a comunicacao spi em modo 0, 0
///
void spi_init(){
  ANS12 = DIGITAL;     // RB0 é digital
  TRISB0 = INPUT;      // RB0 é entrada (DRDY)
  TRISC0 = OUTPUT;     // RC0 para saída (SS)
  TRISC3 = OUTPUT;     // RC3 para saída (SCK)
  TRISC4 = INPUT;      // RC4 para entrada (SDI)
  TRISC5 = OUTPUT;     // RC5 para saída (SDO)
  SS = 1;              // SS inativo 
  SSPEN = 0;           // desabilita modo SPI
  CKP = 0;             // estado inativo é nível LOW
  CKE = 0;             // dado transmitido na borda se subida do SCK
  SMP = 0;             // dado de entrada amostrado no meio do tempo do dado de saída
  SSPCONbits.SSPM = 1; // SPI em modo Master, clock = FOSC/16
  SSPEN = 1;           // habilita modo SPI  
}

void spi_slave_init(){
  ANS12 = DIGITAL;     // RB0 é digital
  TRISB0 = INPUT;      // RB0 é entrada (DRDY)
  TRISC0 = INPUT;      // RC0 para entrada (SS)
  TRISC3 = INPUT;      // RC3 para entrada (SCK)
  TRISC4 = INPUT;      // RC4 para entrada (SDI)
  TRISC5 = OUTPUT;     // RC5 para saída (SDO)
  SSPEN = 0;           // desabilita modo SPI
  CKP = 0;             // estado inativo é nível LOW
  CKE = 0;             // dado transmitido na borda se subida do SCK
  SMP = 0;             // dado de entrada amostrado no meio do tempo do dado de saída
  SSPCONbits.SSPM = 4; // SPI em modo slave
  
  SSPEN = 1;           // habilita modo SPI  
}
void SPI_Slave_Init()
{
  // Set Spi Mode To Slave + SS Enabled 
  SSPM0 = 0;
  SSPM1 = 0;
  SSPM2 = 1;
  SSPM3 = 0;
  // Enable The Synchronous Serial Port
  SSPEN = 1;
  // Configure The Clock Polarity & Phase (SPI Mode Num. 1)
  CKP = 0;
  CKE = 0;
  // Clear The SMP Bit
  SMP = 0;
  // Configure The IO Pins For SPI Master Mode
  ANS12 = DIGITAL;     // RB0 é digital
  TRISB0 = INPUT;      // RB0 é entrada (DRDY)
  TRISC0 = INPUT;      // RC0 para entrada (SS)
  TRISC3 = INPUT;      // RC3 para entrada (SCK)
  TRISC4 = INPUT;      // RC4 para entrada (SDI)
  TRISC5 = OUTPUT;     // RC5 para saída (SDO)
  
  // Enable Interrupts. Comment Them To Disable interrupts(NOT Recommended)
//  SSPIE = 1;;;
//  PEIE = 1;
//  GIE = 1;
}

void spi_interrupt_handler(){
    
    SSPIF=0;
}

///
/// Envia e recebe dado pelo SPI
/// @param data dado a ser transmitido
/// @return retorna dado recebido
///
uint8_t spi_exchange(uint8_t data){
  WCOL = 0;       // limpa flag de colisão
  SS = 0;         // seleção de SPI ativado
  SSPBUF = data;  // transfere dado para o buffer do SPI
  while(SSPSTATbits.BF == 0); // enquanto o buffer não tiver recebido dado, espera
  SS = 1;         // recebeu dado, iniativa seleção
  return SSPBUF;  // retorna o dado recebido
}


//Receive from spi as slave
uint8_t spi_slave_exchange(uint8_t data){
    uint8_t incoming_data = FALSE;
    if(SSPSTATbits.BF){
        incoming_data = SSPBUF;
        SSPBUF = data;
    }
    return incoming_data;
}

//Verify there is data to be read in spi 
int spi_ready(){
    if(SSPSTATbits.BF){
        return TRUE;
    }
    return FALSE;
}

///
/// Faz a leitura de dados por SPI
/// @return retorna dado
///
uint8_t spi_read(){
  
  while (!DATA_READY); // espera os dados estarem prontos para serem lidos
  
  return spi_exchange(DUMMYDATA);
}


///
/// Envia dados por SPI
/// @param data - dado a ser transmitido
///
void spi_write(uint8_t data){
  spi_exchange(data);
}
#endif