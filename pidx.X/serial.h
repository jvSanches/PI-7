//*****************
//function prototypes

void serial_setup(void);
void putch(unsigned char c);
unsigned char getch(void);
void putst(register const char * str);
unsigned char usart_timeout(void);
unsigned char getch_timeout(void);  // [jo:091211]
unsigned char chkchr(void);         // [jo:091211]
void putchdec(unsigned char c);
void putchhex(unsigned char c);
void putinthex(unsigned int c);
void clear_usart_errors();

#define putlf putst("\n") //put line feed



