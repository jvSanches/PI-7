# Pi 7     COMUNICACAO PC-LPC      Grupo3
#Implementação modbus
#
#Conexão Serial método read_register
#

import serial



def LPC_connect():
    #Open Serial port for LPC
    global lpc
    lpc = serial.Serial("COM13", 9600)
    lpc.timeout = 10


def LPC_disconnect():
    #Close Serial port
    lpc.close()

def getChar():
    #If available, reads one char from serial. Else, returns False
        if lpc.in_waiting > 0:
            reading = str(lpc.read())
            return reading
        else:
            return False
def readLine():
    #If available, reads one line from serial. Else, returns False
    if lpc.in_waiting > 0:
        reading = str(lpc.readline())
        return reading
    else:
        return False

def write(data):
    #Write data to serial
    lpc.write(data)

# a = [0xF7, 0x03, 0x13, 0x89, 0x00, 0x0A]
# b = '010300010001' 
def getLRC(messageBytes): 
    #calculates LRC for a byte array
    return 0xff&(0x100-(sum(messageBytes)&0xff))

def GetMessageLRC(message):
    #Calculate LRC for a string
    messageBytes=[]
    for char in message:
        messageBytes.append(ord(char))
    return getLRC(messageBytes)
                
def ReadRegister(slave, regAddres, numOfRegs = 1):
    #Send message asking for a register values
    payload = ("%4.4x" %regAddres)+ ("%4.4x" %numOfRegs)
    fCode=3
    message = buildMessage(slave, fCode, payload)
    transmit(message)
    response = receiveResponse()
    if response and int(response[2:3])==fCode:
        rByteCount = response[4:6]
        rValue = response[6:8]
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

def receiveResponse():
    #Wait for a response. Timeout already set
    myAddres = 1
    incoming = lpc.readline()
    if incoming == 0: return False
    incoming = incoming[1:-2]
    slaveNum = int(incoming[:2])
    
    if slaveNum == myAddres:
        return incoming
    else:
        #Message is not for this slave. Will try again
        return receiveResponse()


def test():
    LPC_connect()
    ReadRegister(1,1)