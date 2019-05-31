# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 15:50:57 2016

@author: Sanches
"""
import time
import msvcrt
import os
import prog_mananger
import machine
import Configurator

loaded_prog = []
def refMachine():
    ''' send a command to move axis to machine`s origin and reset step counters'''
    option = 'start'
    while option != 'r':
        os.system('cls')
        print('Machine will move. Check spindle clearence. Press C to continue or R to return: ' )    
        option = msvcrt.getch().decode('utf-8').lower()    
        if option == 'c':
            machine.ref()
            os.system('cls')
            print('Done. Any key to continue:')
            msvcrt.getch().decode('utf-8').lower()  
            option = 'r'
            
            
def WCS_set():
    selected_WCS = 1    
    while selected_WCS != 'r':
        print('WCSs: \n 4 - G54 \n 5 - G55 \n 6 - G56 \n')
        print('Select WCS to configure: (R  to return)')
          
        selected_WCS = msvcrt.getch().decode('utf-8').lower()
        os.system('cls')
        #print(selected_WCS)
        #time.sleep(5)
        if selected_WCS == '4':
                    
            
            option = 1
            while option != 'r':
                
                print('G54: \n     X : %.3f \n     Y : %.3f \n     Z : %.3f' %(machine.G54[0],machine.G54[1],machine.G54[2]))
                print('\n Select axis : (R to return)')
                option = msvcrt.getch().decode('utf-8').lower()
                if option == 'x':
                    print('x : ')
                    offset = input()
                    if offset != '':
                        machine.G54[0] = (machine.machine_pos[0] - float(offset))
                elif option == 'y':
                    print('y : ')
                    offset = input()
                    if offset != '':
                        machine.G54[1] = (machine.machine_pos[1] - float(offset))
                elif option == 'z':
                    print('z : ')
                    offset = input()
                    if offset != '':
                        machine.G54[2] = (machine.machine_pos[2] - float(offset))
                os.system('cls')
                        
                        
        elif selected_WCS == '5':
            
            option = 1
            while option != 'r':         
                print('G55: \n     X : %.3f \n     Y : %.3f \n     Z : %.3f' %(machine.G55[0],machine.G55[1],machine.G55[2]))
                print('\n Select axis : (R to return)')
                option = msvcrt.getch().decode('utf-8').lower()
                if option == 'x':
                    print('x : ')
                    offset = input()
                    if offset != '':
                        machine.G55[0] = (machine.machine_pos[0] - float(offset))
                elif option == 'y':
                    print('y : ')
                    offset = input()
                    if offset != '':
                        machine.G55[1] = (machine.machine_pos[1] - float(offset))
                elif option == 'z':
                    print('z : ')
                    offset = input()
                    if offset != '':
                        machine.G55[2] = (machine.machine_pos[2] - float(offset))
                        
        elif selected_WCS == '6':
            
            option = 1
            while option != 'r':         
                print('G56: \n     X : %.3f \n     Y : %.3f \n     Z : %.3f' %(machine.G56[0],machine.G56[1],machine.G56[2]))
                print('\n Select axis : (R to return)')
                option = msvcrt.getch().decode('utf-8').lower()
                if option == 'x':
                    print('x : ')
                    offset = input()
                    if offset != '':
                        machine.G56[0] = (machine.machine_pos[0] - float(offset))
                elif option == 'y':
                    print('y : ')
                    offset = input()
                    if offset != '':
                        machine.G56[1] = (machine.machine_pos[1] - float(offset))
                elif option == 'z':
                    print('z : ')
                    offset = input()
                    if offset != '':
                        machine.G56[2] = (machine.machine_pos[2] - float(offset))
        Configurator.saveConfig()
        os.system('cls')
        
def MDI():
        
    prog_MDI = []    
    input_line = 'start'
    while input_line != 'return':
        os.system('cls')
        machine.printPos()
        
        print('MDI program: ')
        
        for i in range(len(prog_MDI)):
            print(prog_MDI[i])
        print('\n ------------------------------------------' )
        print('Input commands:   Run - "run"   Reset - "reset"   Return - "return"\n')
        input_line = input()
        os.system('cls')
        if input_line == 'run':
            prog_mananger.read(prog_MDI)
            machine.allOff()
        elif input_line == 'reset':
            prog_MDI = []
            
        elif input_line == 'return':
            time.sleep(0.01)
        else:
            prog_MDI.append(input_line.upper())
            
        
def JOG():
    option = 'start'    
    jog_step = 1.0
    while option != 'r':
        print(' Press "S" to enter JOG Step, "J" to JOG or "R" to Return: ')        
        option = msvcrt.getch().decode('utf-8').lower()
        os.system('cls')
        if option == 's':
            print('Better use 1/2n, for a real n')
            print('Step = %.3f mm' %(jog_step))
            new_jog_step = input(" New Step: ")
            if new_jog_step != '':
                jog_step =float(new_jog_step)
            os.system('cls')
        elif option == 'j':
            direction = 'start'
            while direction != 'r':
                machine.printPos()
                
                print('JOG %.3f mm ' %(jog_step))                
                print('   8  |             |   7')            
                print('   +  |             |   +')
                print('   Y  | 4 - X + 6   |   Z' )
                print('   -  |             |   -')
                print('   2  |             |   1')
                print('')
                print('Press "R" to return \n')
                
                direction = msvcrt.getch().decode('utf-8').lower()
                if direction != 'r':
                    machine.JOG(direction,jog_step)
                ########################## Mover
                os.system('cls')
    machine.allOff       

def AUTO():
    
    
    option = 'start'
    while option != 'r':
        machine.printPos()
        print('AUTO \n')
        for j in range(len(loaded_prog)):
            print(loaded_prog[j])
        print('\nPress "O" to load a program, "S" to run loaded program and "R" to return') 
        if machine.opt_stop:
                print('OptionalStop ON, "T" to toggle')
        else:
                print('OptionalStop OFF, "T" to toggle')        
        option = msvcrt.getch().decode('utf-8').lower()
        os.system('cls')
        if option == 'o':
            print('Enter program name: ')
            prog_name = 'C:\\Users\\Sanches\\Documents\\My CNC\\M^4\\Programs\\'            
            prog_name += input()
            
            try:
                file = open(prog_name,'r')
                for i in file:
                    loaded_prog.append(i.rstrip())
                for k in range(len(loaded_prog)):
                    loaded_prog[k] = loaded_prog[k].upper()
                file.close()
                os.system('cls')
                
            except:
                print('Failed to open file (any key to continue)')
                msvcrt.getch().decode('utf-8').lower()
                os.system('cls')
                
        if option == 's':
            prog_mananger.read(loaded_prog)
            option = 'r'
            machine.allOff()
            
        if option == 't':
            if machine.opt_stop:
                machine.opt_stop = False
            else:
                machine.opt_stop = True
        #option = 'r'        
                
    
        
        
        
        
        
    
    
    
    