# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 18:42:16 2016

@author: Sanches
"""
import curve_generator
import time
import serial
import os
import msvcrt
#import prog_mananger
#import math
import struct
import Configurator
#import GUI

#Settings: 
mymachine = 0
out_buffer = []
machine_step= 1/4096
    
machine_ready = False

machine_pos = [0,0,0]
machine_steps=[0,0,0]

motion = 0 # G00 , G01, G02, G03, G04

plane = 17   # G17 ,G18 , G19

units = 21  #G20, G21

wcs = 53 # G53, G54, G55, G56

coord = 90 # G90, G91

feed = 94 # G94, G95
standingBy = False
F = 1
act_F=0

S = 0
act_S=0

opt_stop = False

spindle = False

home_pos = [0,0,0]

G53 = [0,0,0]
G54 = [0,0,0]
G55 = [0,0,0]
G56 = [0,0,0]
#G57 = (0,0,0)
#G58 = (0,0,0)

def saveData():
    file = open('Configs', 'w')
    file.write(str(machine_pos[0])+ '\n')
    file.write(str(machine_pos[1])+ '\n')
    file.write(str(machine_pos[2])+ '\n')
    file.write(str(machine_steps[0])+ '\n')
    file.write(str(machine_steps[1])+ '\n')
    file.write(str(machine_steps[2])+ '\n')
    file.write(str(G54[0])+ '\n')
    file.write(str(G54[1])+ '\n')
    file.write(str(G54[2])+ '\n')
    file.write(str(G55[0])+ '\n')
    file.write(str(G55[1])+ '\n')
    file.write(str(G55[2])+ '\n')
    file.write(str(G56[0])+ '\n')
    file.write(str(G56[1])+ '\n')
    file.write(str(G56[2])+ '\n')

    
    
    
    file.close()
    
def loadData():
    global act_F, act_S
    file = open('Configs', 'r')
    parameters= []
    for i in file:
        parameters.append(i.rstrip())
    file.close()
    machine_pos[0] = float(parameters[0])
    machine_pos[1] = float(parameters[1])
    machine_pos[2] = float(parameters[2])
    machine_steps[0] = int(parameters[3])
    machine_steps[1] = int(parameters[4])
    machine_steps[2] = int(parameters[5])
    G54[0] = float(parameters[6])
    G54[1] = float(parameters[7])
    G54[2] = float(parameters[8])
    G55[0] = float(parameters[9])
    G55[1] = float(parameters[10])
    G55[2] = float(parameters[11])
    G56[0] = float(parameters[12])
    G56[1] = float(parameters[13])
    G56[2] = float(parameters[14])

    
    
    
    
        

def delay(delayTime):
    target_time = time.clock() + delayTime
    while time.clock() < target_time:
        pass

def applyWcs(point,wcs,coefs):
    if wcs == 54:
        point[0] += G54[0] * coefs[0]
        point[1] += G54[1] * coefs[1]
        point[2] += G54[2] * coefs[2]
    elif wcs == 55:
        point[0] += G55[0] * coefs[0]
        point[1] += G55[1] * coefs[1]
        point[2] += G55[2] * coefs[2]
    elif wcs == 56:
        point[0] += G56[0] * coefs[0]
        point[1] += G56[1] * coefs[1]
        point[2] += G56[2] * coefs[2]
    return point
    
    
def apply91(X90,Y90,Z90):
    global machine_pos
    X91 = X90 + machine_pos[0]
    Y91 = Y90 + machine_pos[1]
    Z91 = Z90 + machine_pos[2]
    return X91,Y91,Z91


def move(line,line_num):
    ''' move machine to a position given in line'''
    global wcs
    global machine_pos
    global teo_pos
    
    xyz_change = [1,1,1] 
    
    for i in range(2,5):
        if line[i] == '' and line[13] == 90:
            line[i] = teo_pos[i-2]
            xyz_change[i-2] = 0
        elif line[i] == '' and line[13] == 91:
            line[i] = 0
            xyz_change[i-2] = 0
    teo_pos = [line[2], line[3], line[4]]
    teo_pos = applyWcs(teo_pos,wcs,xyz_change)
    print(teo_pos)
    if line[1] != 0 and line[1] != 1:
        xyz_change= [1,1,1]
            
    if line[13] == 91:
        line[2],line[3],line[4] = apply91(line[2],line[3],line[4])
    abs_point = applyWcs([line[2],line[3],line[4]],wcs,xyz_change)  
    #print('aaa', line[2],line[3],line[4],abs_point)
    
    # print(abs_point)

    

    pack_to_send = '2 '
    pack_to_send +=  '%d %.3f %.3f %.3f %.3f %.3f ' %((line[1]),abs_point[0],abs_point[1],abs_point[2], line[5], line[6])
    message = bytes(pack_to_send, 'utf-8')
    out_buffer.append(message)
    

    '''
    steps = curve_generator.generate_move(line[1],abs_point[0],abs_point[1],abs_point[2],line[5],\
    line[6],line[7])
    
    
    
    
    if line[1]== 0:        
        step_delay = 0.0001
    else:
        step_delay = 60/(4096*F)
        if step_delay < 0.001:
            step_delay = 0.001
    
    all0x = True  
    all0y = True 
    all0z = True 
      
    for i in range(len(steps)):
        if steps[i][0] != 0:
            all0x = False
        if steps[i][1] != 0:
            all0y = False
        if steps[i][2] != 0:
            all0z = False
            
    xyz_state = 111 - (all0x * 100 + all0y * 10 + all0z *1)       
    
       
    
    machine.write(struct.pack('>2B', 91, xyz_state))
        
    
    
    for i in range(len(steps)):
        xyz_move = (1 + steps[i][0]) * 100 + (1 + steps[i][1]) * 10 + (1 + steps[i][2]) * 1
        machine.write(struct.pack('>B', xyz_move))
        #delay(0.001)
        
        machine_pos[0] += steps[i][0] * machine_step
        machine_pos[1] += steps[i][1] * machine_step
        machine_pos[2] += steps[i][2] * machine_step
        
    Configurator.savePos()
    
    os.system('cls')
    printPos()
    

def JOG(direction, jog_step):
    if direction == '6':
        step = [1,0,0]
        xyz_state = 100
    elif direction == '4':
        step = [-1,0,0]
        xyz_state = 100
    elif direction == '8':
        step = [0,1,0]
        xyz_state = 10
    elif direction == '2':
        step = [0,-1,0]
        xyz_state = 10
    elif direction == '7':
        step = [0,0,1]
        xyz_state = 1
    elif direction == '1':
        step = [0,0,-1]
        xyz_state = 1
    else:
        step = [0,0,0]
        xyz_state = 0
        
    xyz_move = (1 + step[0]) * 100 + (1 + step[1]) * 10 + (1 + step[2]) * 1
    numOfSteps = int(jog_step / machine_step)   
    machine.write(struct.pack('>2B', 91, xyz_state))
    for i in range(numOfSteps):
        
        machine.write(struct.pack('>B', xyz_move))
        #delay(0.001)
        
        machine_pos[0] += step[0] * machine_step
        machine_pos[1] += step[1] * machine_step
        machine_pos[2] += step[2] * machine_step
        
    Configurator.savePos()
        
        
def printPos():
    print('X : %.3f \nY : %.3f \nZ : %.3f '\
    %(machine_pos[0],machine_pos[1],machine_pos[2]))
    #print(prog_mananger.prog_to_print[line_num])
        
'''
        
def goHome(line_num):
    line_param =  [0,0  ,home_pos[0],home_pos[1],home_pos[2] ,0 ,0 , 0,0 ,0 ,17    , 53 , 21 , 90    , 94       ]
    move(line_param,line_num)
    #print('Vai pra casa')    
    
    
    
def startSpindle():
    global spindle    
    spindle = True
    set_spindle()
    
def stopSpindle():
    global spindle    
    spindle = False
    set_spindle()
    

def set_spindle():    
    ''' if M3 sends s to machine. else, sends 0'''
    if spindle:
        pack_to_send = '4 ' + str(S)
        message = bytes(pack_to_send, 'utf-8') 
        #print(message)   
        out_buffer.append(message)


        #print('liga spindle')
        
    else:
        pack_to_send = '4 ' + str(0)
        message = bytes(pack_to_send, 'utf-8')    
        out_buffer.append(message)
        
        
def connection():
    global machine
    global machine_ready
    option = 'start'
    port = 'COM4'
    while option != 'r':
        os.system('cls')
        if machine_ready:
            print('Machine connected')
        else:
            print('Machine not connected')
        print('Press "C" to connect/disconnect, "P" to select port. "R" to return')
        option = msvcrt.getch().decode('utf-8').lower()
        if option == 'c':
            if not machine_ready:
                try:
                    machine = serial.Serial(port,9600)
                                        
                    machine_ready = True
                except:
                    os.system('cls')
                    print('Connection failed. Any key to continue')
                    msvcrt.getch().decode('utf-8').lower()
                
            else:
                machine.close()
                machine_ready = False
        elif option == 'p':
            os.system('cls')
            print('Type port to connect:')
            port = input()
            
def ref():
    machine.write(struct.pack('>2B', 91 , 111))
    delay(0.01)
    machine.write(struct.pack('>B', 222))
    machine.write(struct.pack('>2B', 92 , 127))
    delay(1)
    machine.write(struct.pack('>2B',91, 0))
    machine.write(struct.pack('>2B', 92 , 0))
     
def allOff():
    machine.write(struct.pack('>2B', 91, 0))

def update():
    pass