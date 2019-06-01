# Pi 7     COMUNICACAO PC-LPC      Grupo3
# Clara Ploretti Cappato - 9833534
# Guilherme de Agrela Lopes 9833513
# João Vitor Sanches - 9833704
# Lucas Eder Alves - 9345731
# Matheus Alves Ivanaga - 9836836
# Victor Chacon Codesseira - 9833711
# Victor Figueiredo Soares - 9833322
#Implementação modbus
#
#Conexão Serial método read_register e writeSingleRegister
#LRC e demais verificações funcionando

import serial
from time import sleep

def LPC_connect(port):
    #Open Serial port for LPC
    global lpc
    lpc = serial.Serial(port, 9600)
    lpc.timeout = 3


def LPC_disconnect():
    #Close Serial port
    lpc.close()

def LPC_getChar():
    #If available, reads one char from serial. Else, returns False
        if lpc.in_waiting > 0:
            reading = str(lpc.read())
            return reading
        else:
            return False

def LPC_readLine():
    #If available, reads one line from serial. Else, returns False
    return lpc.readline().decode('utf-8')


def LPC_write(data):
    #Write data to serial
    lpc.write(data.encode('utf-8'))

# a = [0xF7, 0x03, 0x13, 0x89, 0x00, 0x0A]
# b = '010300010001'
def getLRC(messageBytes):
    #calculates LRC for a byte array
    return 0xff&(0x100-(sum(messageBytes)&0xff))

def LPC_waiting():
    if lpc.in_waiting >12:
        return True
    else:
        return False

def GetMessageLRC(message):
    #Calculate LRC for a string
    messageBytes=[]
    for char in message:
        messageBytes.append(ord(char))
    return getLRC(messageBytes)

def ReadRegister(slave, regAddress, numOfRegs = 1):
    #Send message asking for a register values
    payload = ("%4.4x" %regAddress)+ ("%4.4x" %numOfRegs)
    fCode=3
    message = buildMessage(slave, fCode, payload)
    transmit(message)
    #sleep(2)
    response = receiveResponse()

    if response and int(response[2:4],16)==fCode:
        rByteCount = int(response[4:8],16)
        rValue = int(response[8:12],16)
        return rValue
    else:
        #Pass response to correct handler
        print("Returned wrong function code")
        return False

def buildMessage(slave, fCode, payload):
    #Prepares a message for transmission
    message = ("%2.2x" %slave)+ ("%2.2x" %fCode)+ payload
    txLRC=GetMessageLRC(message)
    message=':' + message + ("%2.2x" %txLRC) + '\r\n'
    return message

def transmit(message):
    #Send message
    print("Data trasmitted: ", [hex(ord(no)) for no in message])
    LPC_write(message)
    sleep(5)

def receiveResponse():
    #Wait for a response. Timeout returns False
    myAddres = 1
    incoming = LPC_readLine()
    #incoming= incoming.decode()
    if incoming == 0: return False
    print("Message from LPC: ", incoming[:-2])
    incoming = incoming[1:-2]
    slaveNum = int(incoming[:2])
    if slaveNum == myAddres:
        if checkLRC(incoming): return incoming
        else:
            print("LRC missmatch")
            return False
    else:
        #Message is not for this slave. Will try again
        return receiveResponse()

def checkLRC(rMessage):
    #Receive the message without : an \r\n.
    rLRC = int(rMessage[-2:],16)
    cLRC = GetMessageLRC(rMessage[:-2])
    return rLRC==cLRC

def WriteSingleRegister(slave, regAddress,nValue):
    payload = ("%4.4x" %regAddress)+ ("%4.4x" %nValue)
    fCode=6
    message = buildMessage(slave, fCode, payload)
    transmit(message)
    #response = receiveResponse()
    # if response and int(response[2:4],16)==fCode:
    #     rRegAddr = int(response[4:8],16)
    #     rValue = int(response[8:12],16)
    #     return rValue
    # else:
    #     #Pass response to correct handler
    #     print("Returned wrong function code")
    #     return False
    return

def sendLines(slave, coords):
    fCode=0x15
    for line in coords:
        payload = ("%4.4x" %line[0]) # + ("%4.4x" %line[1]) + ("%4.4x" %line[2])
        message = buildMessage(slave, fCode, payload)
        transmit(message)
        
        # response = receiveResponse()
        # if response and int(response[2:4],16)==fCode:
        #     rRegAddr = int(response[4:8],16)
        #     rValue = int(response[8:12],16)
        #     return rValue

        # else:
        #     #Pass response to correct handler
        #     print("Returned wrong function code")
        #     return False

def test():
    LPC_connect("COM13")
    print(ReadRegister(1,1))     #prints register 1 value
    # LPC_disconnect()

'''
#################################################################
Exemplo de uso das funções implementadas

PS D:\Poli\PI-7\Python_sender> python -i  .\modbus_sender.py
>>> LPC_connect()
>>> print(ReadRegister(1,1))
Data trasmitted:  ['0x3a', '0x30', '0x31', '0x30', '0x33', '0x30', '0x30', '0x30', '0x31', '0x30', '0x30', '0x30', '0x31', '0x62', '0x61', '0xd', '0xa']
Message from LPC:  :010300010043B4
67
>>> print(ReadRegister(1,9))
Data trasmitted:  ['0x3a', '0x30', '0x31', '0x30', '0x33', '0x30', '0x30', '0x30', '0x39', '0x30', '0x30', '0x30', '0x31', '0x62', '0x32', '0xd', '0xa']
Message from LPC:  :01030001000EA6
14
>>> WriteSingleRegister(1,9,78)
Data trasmitted:  ['0x3a', '0x30', '0x31', '0x30', '0x36', '0x30', '0x30', '0x30', '0x39', '0x30', '0x30', '0x34', '0x65', '0x37', '0x37', '0xd', '0xa']
Message from LPC:  :01060009004E97
78
>>> print(ReadRegister(1,9))
Data trasmitted:  ['0x3a', '0x30', '0x31', '0x30', '0x33', '0x30', '0x30', '0x30', '0x39', '0x30', '0x30', '0x30', '0x31', '0x62', '0x32', '0xd', '0xa']
Message from LPC:  :01030001004EA2
78
>>>
'''
