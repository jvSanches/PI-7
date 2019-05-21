/*
  POSITION SENSOR IMPLEMENTATION
  
  obs.: Nao consegui encontrar uma forma de fazer
  referencias externas a variaveis volatile static.
  Assim, como o sensor eh atualizado na rotina de interrupcao,
  foi incluida a implementacao diretamente no main.
  Inclui em um arquivo separado para sugerir a modularizacao
*/

volatile static _POSITION pos_currentPosition;
volatile static unsigned char pos_previousEncoder;
volatile static unsigned char pos_currentEncoder;
volatile static unsigned char pos_inA;
volatile static unsigned char pos_inB;
//HTC volatile static signed char encoderStates[4][4];
volatile static signed char encoderStates[4][4];
volatile static int menos1 = -1;

_POSITION pos_getCurrentPosition() {
  return pos_currentPosition;
} // pos_getCurrentPosition

void pos_setCurrentPosition(_POSITION pos) {
  pos_currentPosition = pos;
} // pos_setCurrentPosition

void pos_init() {
  unsigned char i, j;

  pos_currentPosition = 0;
  pos_previousEncoder = 0;
  for (i=0; i<4; i++)
    for(j=0; j<4; j++)
      encoderStates[i][j] = 0;

  encoderStates[0][1] = 1;
  encoderStates[1][3] = 1;
  encoderStates[3][2] = 1;
  encoderStates[2][0] = 1;

// XC8 atribuindo menos1 ao inves de -1 evita warning 1395 (code sequence generated not well tested)
  encoderStates[2][3] = menos1;
  encoderStates[3][1] = menos1;
  encoderStates[1][0] = menos1;
  encoderStates[0][2] = menos1;

} // pos_init