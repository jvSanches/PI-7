
#ifndef SPI_H
#define SPI_H

#define SSP_RNE (1<<2)
#define SSP_BSY (1<<4)

void spi_init();
void spi_txrx(uint8_t* tx, uint8_t* rx, uint16_t len);
uint8_t spi_bytetx( uint8_t tx);
void spi_select(uint8_t CS);
#endif
