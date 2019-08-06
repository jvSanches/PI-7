///
/// Asynchonous serial channel header file
///
#ifndef SERIAL_H
#define SERIAL_H

/// Initialize an asynchronous serial channel
void serial_init(void);

/// Get an 8-bit character
/// IMPORTANT: it does not return if a character is not received
unsigned char getch(void);

/// Get an 8-bit character
/// It waits a timeout for the chacater to arrive.
/// If no chacarter arrives within the timeout,
/// this function returns 255.
/// 
unsigned char getch_timeout(void);

/// If there has been a previous timeout error from getch_timeout(),
/// this function returns TRUE
unsigned char usart_timeout(void);

/// Check and return an 8-bit character
/// If no character is ready in the input buffer
/// this function returns 255.
/// IMPORTANT: it always return without waiting
///
unsigned char chkchr(void);

/// Send an 8-bit character
void putch(unsigned char c);

/// Send a string
void putst(register const char * str);

/// Send a character in decimal form
void putchdec(unsigned char c);

/// Send a character in hexadecimal form
void putchhex(unsigned char c);

/// Send a integer number as hexadecimal form
void putinthex(unsigned int c);

/// Put a line feed
#define putlf putst("\n")

#endif