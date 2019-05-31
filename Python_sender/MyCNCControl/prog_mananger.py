# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 10:17:07 2016

@author: Sanches
"""
import os
import machine
# import GUI


prog_to_print = []

def refine(prog):
    ''' breaks a program into lists of lists of strings'''
    refined_prog = []
    for i in range(len(prog)):
        line = []
        module = ''
        comment = False
        for j in range(len(prog[i])):            
            
            if prog[i][j] == '(':
                comment = True
            if comment and prog[i][j] == ')':
                comment = False
            
            if not comment:            
                if 65 <= ord(prog[i][j]) <= 90:
                    if module != '':
                        line.append(module)
                    module = prog[i][j]
                elif 48 <=ord(prog[i][j]) <= 57 or prog[i][j] == '.' or prog[i][j] == '-':
                    module += prog[i][j]            
        if len(module)> 1:
            line.append(module)                   
        refined_prog.append(line)
    return(refined_prog)
    
    
def manange(prog):
    '''create a table of parameters
            [N, G , X, Y, Z, I, J, K, F, S, plane, wcs, unit, coord, feedmode] 
            [0, 1 , 2, 3, 4, 5, 6, 7, 8, 9, 10   , 11 , 12 , 13    , 14      ]''' 
    initial_param = [0,0  ,'' ,'','' ,0 ,0 , 0,0 ,0 ,17    , 53 , 21 , 90    , 94       ]
    param=[]
    for i in range(len(prog)):
        
            
        #prog[i] = prog[i].upper()
        global prog_to_print
        print(prog_to_print[i])
                
        if i == 0:        
            line_param = initial_param
        else: 
            line_param = param[i-1]
            line_param[2] = line_param[3] = line_param[4] = ''
            line_param[5] = line_param[6] = line_param[7] = 0
            
        for j in range(len(prog[i])):
            
            func= prog[i][j][0]
            
            value=''
            for k in range(1,len(prog[i][j])):
                value += prog[i][j][k]
            
            value = float(value)
            #print(func,value)
            
            
            if func == 'N':
                line_param[0] = int(value)
            if func == 'G':
                if 0 <= value <= 4:
                    line_param[1] = int(value)
                if 17 <= value <= 19:
                    line_param[10] = int(value)
                if value == 28:
                    machine.goHome(i)
                if 53 <= value <= 56:
                    line_param[11] = machine.wcs = int(value)
                if 20 <= value <= 21:
                    line_param[12] = int(value)
                if 94 <= value <= 95:
                    line_param[14] = int(value)
                if 90 <= value <= 91:
                    line_param[13] = int(value)
                    
            if func == 'X':
                line_param[2] = value
            if func == 'Y':
                line_param[3] = value
            if func == 'Z':
                line_param[4] = value
            if func == 'I':
                line_param[5] = value
            if func == 'J':
                line_param[6] = value
            if func == 'K':
                line_param[7] = value
            if func == 'F':
                line_param[8] = int(value)
            if func == 'S':
                if value != param[i-1][9]:
                    line_param[9] = int(value)
                    machine.S = value
                    machine.set_spindle()
                
            
            
            
            if func == 'M':
                if value == 0:
                    print('M0 stop. Press enter to continue:')
                    input()   
                if value == 1:
                    if machine.opt_stop:
                        print('M1 stop. Press enter to continue:')
                        input() 
                    
                if value == 3:
                    machine.startSpindle()
                    
                if value == 5:
                    machine.stopSpindle()
                    
                if value == 30:
                    machine.goHome(i)
                    machine.stopSpindle()
                    
        if line_param[2] != '' or line_param[3] != '' or line_param[4] != '':
                print('movendo')                
                machine.move(line_param,i)    
           
        
        
        param.append(line_param[:])

        
def read(loaded_prog):     
    machine.teo_pos = machine.machine_pos
    global prog_to_print
    prog_to_print = loaded_prog[:]
    manange(refine(loaded_prog))
