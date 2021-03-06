/**
 * Modulo: Comunicacao MODBUS (simplificada)
 *
 * PI-7     Grupo 3
 *
# Clara Ploretti Cappato - 9833534
# Guilherme de Agrela Lopes 9833513
# João Vitor Sanches - 9833704
# Lucas Eder Alves - 9345731
# Matheus Alves Ivanaga - 9836836
# Victor Chacon Codesseira - 9833711
# Victor Figueiredo Soares - 9833322
 * Funções alteradas para coerencia com protocolo modbus e implemetação das funções auxiliares
 *
 */

#define byte uint8_t
/*
 * FreeRTOS includes
 */
#include "FreeRTOS.h"
#include "queue.h"
#include <stdio.h>

// Drivers for UART, LED and Console(debug)
#include <cr_section_macros.h>
#include <NXP/crp.h>
#include "LPC17xx.h"
#include "type.h"
#include "drivers/uart/uart.h"
//#include "drivers/console/basic_io.h"
#include "drivers/ledonboard/leds.h"

// Includes for PI7
#include "modbus.h"
#include "pi7/interpretador_comando/interpretador_comando.h"
#include "pi7/programa_trajetoria/programa_trajetoria.h"
#include "pi7/estado_trajetoria/estado_trajetoria.h"

// CommModes: Dev_mode para debug; escreve na console
//            Real_mode para execucao real
#define DEVELOPMENT_MODE 0
#define REAL_MODE 1


// *** Configuracao da serial (_mode = REAL_MODE)
#define BAUD 9600
#define MAX_RX_SIZE 1000

// *** endereco deste node
#define MY_ADDRESS 0x01

// Function Codes
#define READ_REGISTER 0x03
#define WRITE_REGISTER 0x06
#define WRITE_FILE 0x15

// Defines de uso geral
#define NO_CHAR -1

// Estados do canal de recepcao
#define HUNTING_FOR_START_OF_MESSAGE 0
#define HUNTING_FOR_END_OF_MESSAGE 1
#define IDLE 3
#define MESSAGE_READY 4


int _state;
int _mode;
byte rxBuffer[MAX_RX_SIZE];
int idxRxBuffer;
byte txBuffer[1024];
int idxTxBuffer;
extern xQueueHandle qCommDev;

/************************************************************************
 decode, encodeLow, encodeHigh
 Transforma de/para o codigo ASCII de 2 bytes usado no protocolo
 Parametros de entrada:
    decode: high, low
    encodeLow, encodeHigh, value
 Retorno:
    decode: (byte) conversao de 2 bytes ASCII para 1 byte
    encodeLow, encodeHigh: (byte) valor convertido de 1 byte para 1 byte ASCII
*************************************************************************/
byte decode(byte high, byte low) {
   byte x, y;
   if (low < 'A') {
      x = (low & 0x0f);
   } else {
      x = (low & 0x0f) + 0x09;
   }
   if ( high < 'A') {
      y = (high & 0x0f);
   } else {
      y = (high & 0x0f) + 0x09;
   }
   return ( x | ( y << 4) );
} // decode

byte encodeLow(byte value) {
   byte x;
   x = value & 0x0f;
   if ( x < 10) {
      return (0x30 + x);
   } else {
      return (0x41 + (x-10));
   }
} // encodeLow

byte encodeHigh(byte value) {
   byte x;
   x = ((value & 0xf0) >> 4);
   if ( x < 10) {
      return (0x30 + x);
   } else {
      return (0x41 + (x-10));
   }
} // encodeHigh

/************************************************************************
 putCharToSerial
 Escreve o conteudo atual do txBuffer na serial, de acordo com _mode
 _mode = DEV_MODE : printf na console de debug
 _mode = REAL_MODE : escreve da UART0
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
void putCharToSerial() {

  if (_mode == DEVELOPMENT_MODE ) {
//     vPrintString(txBuffer);
//     vPrintString("\r");
  } else {

//     UARTSendNullTerminated(0, txBuffer);
  }
} // putCharToSerial

/************************************************************************
 getCharFromSerial
 Obtem um caracter da interface serial. A interface a utilizar depende de
 _mode = DEV_MODE : obter caracter da fila qCommDev
 _mode = REAL_MODE : obter da UART0
 Parametros de entrada:
    nenhum
 Retorno:
    (int) caracter obtido ou NO_CHAR se nenhum caracter disponivel
*************************************************************************/
int getCharFromSerial() {
  char ch;

  if (_mode == DEVELOPMENT_MODE ) {
	  xQueueReceive(qCommDev, &ch, portMAX_DELAY);
	  return (int)ch;
  } else {
      return UARTGetChar(0, FALSE);
  }
} // getCharFromSerial

/************************************************************************
 calculateLRC, checkLRC
 Calcula e verifica o checksum
 Parametros de entrada:
    calculateLRC: (byte[]) bytes, (int) start, (int) end
    checkLRC: nenhum
 Retorno:
    calculateLRC: (byte) LRC calculado
    checkLRC: TRUE se correto, FALSE caso contrario
*************************************************************************/
byte calculateLRC(byte* frame, int start, int end) {
  byte accum;
  byte ff;
  byte um;
  int i;
  accum = 0;
  ff = (byte)0xff;
  um = (byte)0x01;

  for (i= start; i < end; i++) {
     accum += frame[i];
  }
  accum = (byte) (ff - accum);
  accum = accum + um;
  return accum;
} // calculateLRC


byte myLRC (byte *nData, int start, int end)
{
byte nLRC = 0 ; // LRC char initialized

for (int i= start; i < end; i++)
nLRC += nData[i];

return (byte)(-nLRC);

} // End: LRC

int checkLRC() {
  int retval;
  byte receivedLRC;
  byte calculatedLRC;


  if (_mode == DEVELOPMENT_MODE) {
	  // do not check LRC in DEV mode
	  return TRUE;
  }
  retval = FALSE;
  receivedLRC = decode(rxBuffer[idxRxBuffer-3], rxBuffer[idxRxBuffer-2]);
  calculatedLRC = myLRC(rxBuffer, 1, idxRxBuffer - 3);//calculateLRC(rxBuffer, 1, idxRxBuffer - 3);

  if ( receivedLRC == calculatedLRC) {
     retval = TRUE;
  }
  return retval;
} // checkLRC

/************************************************************************
 processReadRegister, processWriteRegister, processWriteFile
 As funcoes realizam o processamento das mensagens
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
void processReadRegister() {
   int registerToRead;
   int registerValue;
   byte lrc;

   registerToRead = decode ( rxBuffer[7], rxBuffer[8]);
   // Aciona controller para obter valor. Note que a informacao
   // ate´ poderia ser acessada diretamente. Mas a arquitetura MVC
   // exige que todas as interacoes se deem atraves do controller.
   registerValue = ctl_ReadRegister(registerToRead);

   // Monta frame de resposta e a envia
   txBuffer[0] = ':';
   txBuffer[1] = encodeHigh(MY_ADDRESS);
   txBuffer[2] = encodeLow(MY_ADDRESS);
   txBuffer[3] = encodeHigh(READ_REGISTER);
   txBuffer[4] = encodeLow(READ_REGISTER);
   txBuffer[5] = encodeHigh(0);
   txBuffer[6] = encodeLow(0);
   txBuffer[7] = rxBuffer[7]; // byte count field  (high part)
   txBuffer[8] = rxBuffer[8];  // byte count field (low part)
   txBuffer[9] = encodeHigh(registerValue >>8 );
   txBuffer[10] = encodeLow(registerValue >> 8);
   txBuffer[11] = encodeHigh(registerValue & 0xff);
   txBuffer[12] = encodeLow(registerValue & 0xff);
   lrc = myLRC(txBuffer, 1, 13);
   txBuffer[13] = encodeHigh(lrc);
   txBuffer[14] = encodeLow(lrc);
   txBuffer[15] = 0x0d;
   txBuffer[16] = 0x0a;
   txBuffer[17] = 0; // null to end as string

   putCharToSerial();
} // processReadRegister

void processWriteRegister() {
	   int registerToWrite;
	   int registerValue;
	   byte lrc;

	   registerToWrite = decode ( rxBuffer[7], rxBuffer[8]);
	   registerValue = decode(rxBuffer[11], rxBuffer[12]);

	   // Aciona controller porque a arquitetura MVC
	   // exige que todas as interacoes se deem atraves do controller.
	   if (ctl_WriteRegister(registerToWrite, registerValue)){

		   // Monta frame de resposta e a envia
		   txBuffer[0] = ':';
		   txBuffer[1] = encodeHigh(MY_ADDRESS);
		   txBuffer[2] = encodeLow(MY_ADDRESS);
		   txBuffer[3] = encodeHigh(WRITE_REGISTER);
		   txBuffer[4] = encodeLow(WRITE_REGISTER);
		   txBuffer[5] = encodeHigh(0);
		   txBuffer[6] = encodeLow(0);
		   txBuffer[7] = encodeHigh(registerToWrite);
		   txBuffer[8] = encodeLow(registerToWrite);
		   txBuffer[9] = encodeHigh(0);
		   txBuffer[10] = encodeLow(0);
		   txBuffer[11] = encodeHigh(registerValue);
		   txBuffer[12] = encodeLow(registerValue);
		   lrc = myLRC(txBuffer, 1, 13);
		   txBuffer[13] = encodeHigh(lrc);
		   txBuffer[14] = encodeLow(lrc);
		   txBuffer[15] = 0x0d;
		   txBuffer[16] = 0x0a;
		   txBuffer[17] = 0; // null to end as string
		   putCharToSerial();
	   }
} // processWriteRegister

void processWriteFile() {
	int newX, newY, newZ;
	newX = (decode(0x30, rxBuffer[5]) << 8 );
	newX |= (decode(rxBuffer[6], rxBuffer[7]));
	newY = (decode(0x30, rxBuffer[8]) << 8 );
	newY |= (decode(rxBuffer[9], rxBuffer[10]));
	newZ = (decode(0x30, rxBuffer[11]));

	printf("X:%d Y:%d Z:%d \n", newX-2048, newY-2048, newZ);
	ptj_storeProgram(newX-2048, newY-2048, newZ);
	} // processWriteProgram

/************************************************************************
 decodeFunctionCode
 Extrai o function code
 Parametros de entrada:
    nenhum
 Retorno:
    (int) retorna o function code
*************************************************************************/
int decodeFunctionCode() {
   return decode(rxBuffer[3], rxBuffer[4]);
} // extractFunctionCode



/************************************************************************
 processMessage
 Processa uma mensagem ModBus. Inicialmente, verifica o checksum.
 Se estiver correto, aciona a funcao que realiza o processamento
 propriamente dito, de acordo com o function code especificado
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
 void processMessage() {
    int functionCode;
    if ( checkLRC() ) {
       functionCode = decodeFunctionCode();
       switch (functionCode) {
         case READ_REGISTER:
             processReadRegister();
             break;
         case WRITE_REGISTER:
             processWriteRegister();
             break;
         case WRITE_FILE:
             processWriteFile();
             break;

       } // switch on FunctionCode
    }
    _state = HUNTING_FOR_START_OF_MESSAGE;
 } // processMessage

/************************************************************************
 receiveMessage
 Recebe uma mensagem, byte a byte. Notar que, para o multi-tasking
 cooperativo funcionar, cada funcao deve retornar o mais rapidamente possivel.
 Isso ate nem seria necessario com o FreeRTOS, mas exemplifica a ideia de
 multitasking cooperativo.
 Assim, a recepcao não fica em loop esperando terminar de receber toda a mensagem.
 A mensagem recebida vai sendo armazenada em rxBuffer; idxRxBuffer indica
 em que posicao armazenar o caracter recebido. Ao verificar que a msg foi
 completada (recebendo 0x0D, 0x0A), sinaliza que a msg foi
 recebida fazendo _state = MESSAGE_READY.
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
void receiveMessage() {
   char ch;
   int chInt;
   chInt = getCharFromSerial();

//   if (chInt > 0){
//   printf("got %x\n", (char)chInt);
//   }

   if (chInt != NO_CHAR ) {
      ch = (char)chInt;
      if (_state == HUNTING_FOR_START_OF_MESSAGE) {
         if ( ch == ':' ) {
            idxRxBuffer = 0;
            rxBuffer[idxRxBuffer] = ch;
            _state = HUNTING_FOR_END_OF_MESSAGE;
            return;
         }
      } else if (_state == HUNTING_FOR_END_OF_MESSAGE) {
         idxRxBuffer++;
         if ( idxRxBuffer > MAX_RX_SIZE ) {
            _state = HUNTING_FOR_START_OF_MESSAGE;
            idxRxBuffer = 0;
            return;
         }
         if ( ch == ':' ) {
        	 idxRxBuffer = 0;
         }
         rxBuffer[idxRxBuffer] = ch;
         if ( (rxBuffer[idxRxBuffer] == 0x0A) && ( rxBuffer[idxRxBuffer-1] == 0x0D) ) {
            _state = MESSAGE_READY;
         }
      }
   } // if NO_CHAR
} // receiveMessage

/************************************************************************
 initCommunication
 Inicializa modulo de comunicacaoes
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
void com_init() {
   _state = HUNTING_FOR_START_OF_MESSAGE;
   _mode = REAL_MODE;  //DEVELOPMENT_MODE
   if (_mode == REAL_MODE ) {
     UARTInit(0, BAUD);
   }
} // initCommunication

/************************************************************************
 executeCommunication
 Recebeu uma requisicao ModBus e a processa
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
void com_executeCommunication() {
   receiveMessage();
   if ( _state == MESSAGE_READY ) {
       processMessage();
   }
} // executeCommunication


/************************************************************************
 sendReport
 Transmite a posicao e a linha atual para o canal serial
*************************************************************************/
void sendReport(){
	char report[30];
	sprintf(report, "X: %4d Y: %4d Z: %2d L: %3d ", stt_getX(), stt_getY(),stt_getZ(), stt_getCurrentLine());
	report[28] = 0x0d;
	report[29] = 0x0a;
	UARTSend(0, report, 30);
}
