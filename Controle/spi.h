/* 
 * File:     spi.h 
 * Author:   Bruno Alan Miyamoto
 * Date:     7/02/2016
 * Comments: Controla interface SPI
 * Revision history: 
 */

#ifndef SPI_H
#define	SPI_H

#include <xc.h> 
#include <stdint.h>

void spi_init(); ///< inicializa o spi no modo 0,0 master

uint8_t spi_exchange(uint8_t data); ///< transmite e recebe por spi

uint8_t spi_read(); ///< lê byte pelo SPI

int spi_ready();// Usado para verificação de dados para serem lidos

uint8_t spi_slave_exchange(uint8_t data);//Recebe e transmite como slave

void spi_write(uint8_t data); ///< escreve byte pelo SPI

#endif