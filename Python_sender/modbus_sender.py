# Pi 7     COMUNICACAO PC-LPC      Grupo3
# Clara Ploretti Cappato - 9833534
# Guilherme de Agrela Lopes 9833513
# João Vitor Sanches - 9833704
# Lucas Eder Alves - 9345731
# Matheus Alves Ivanaga - 9836836
# Victor Chacon Codesseira - 9833711
# Victor Figueiredo Soares - 9833322
# Implementação modbus
#

import serial
from time import sleep

# Conecta no serial da LPC
def LPC_connect(port):
    global lpc
    lpc = serial.Serial(port, 9600)
    lpc.timeout = 0.1

# Fecha conexão
def LPC_disconnect():
    lpc.close()

# Lê uma linha do serial
def LPC_readLine():
    if lpc.in_waiting > 0:
        return lpc.readline().decode('utf-8')
    return False

# Escreve dados no serial
def LPC_write(data):
    #Write data to serial
    lpc.write(data.encode('utf-8'))

# Calcula LRC de uma string
def getLRC(messageBytes):
    return 0xff&(0x100-(sum(messageBytes)&0xff))

# Calcula LRC da mensagem
def GetMessageLRC(message):
    messageBytes=[]
    for char in message:
        messageBytes.append(ord(char))
    return getLRC(messageBytes)

# Lê registrador do ModBus
def ReadRegister(slave, regAddress, numOfRegs = 1):
    payload = ("%4.4x" %regAddress)+ ("%4.4x" %numOfRegs)
    fCode=3
    message = buildMessage(slave, fCode, payload)
    transmit(message)

# Escreve um registrador do ModBus
def WriteSingleRegister(slave, regAddress,nValue):
    payload = ("%4.4x" %regAddress)+ ("%4.4x" %nValue)
    fCode=6
    message = buildMessage(slave, fCode, payload)
    transmit(message)
    return

# Prepara mensagem para envio
def buildMessage(slave, fCode, payload):
    message = ("%2.2x" %slave)+ ("%2.2x" %fCode)+ payload
    txLRC=GetMessageLRC(message)
    message=':' + message + ("%2.2x" %txLRC) + '\r\n'
    return message

# Envia mensagem
def transmit(message):
    print("Data trasmitted: ", [hex(ord(no)) for no in message])
    LPC_write(message)
    sleep(0.1)

# Envia linhas para a LPC
def sendLines(slave, coords):
    fCode=0x15
    for line in coords:
        payload = ("%3.3x" %line[0])  + ("%3.3x" %line[1]) + ("%1.1x" %line[2])
        message = buildMessage(slave, fCode, payload)
        transmit(message)

# Obtém coordenadas, do serial
def receiveXYZ():
    nx = ny = nz = nl = None
    if lpc.in_waiting> 0:
        rx = LPC_readLine()
        if rx[0] != ':':              
            nx = int(rx[2:7])/10
            ny = int(rx[10:15])/10
            nz = int(rx[18:21])/10
            nl = int(rx[24:28])
    return nx, ny, nz, nl