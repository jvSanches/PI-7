import minimalmodbus

minimalmodbus.BAUDRATE = 9600
lpc = minimalmodbus.Instrument("COM15", 1, 'ascii')
lpc.serial.timeout = 10
lpc.serial.parity='E'
lpc.debug = 1
resp = lpc.read_register(1)

