# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 15:31:12 2016

@author: Sanches
"""
import Functions
import msvcrt
import os
import machine
import Configurator

  
def mainMenu():
    os.system('cls')
    mode = 1
    while mode != 0:
        print(' Options: \n 1 - REF \n 2 - WCS Settings  \
        \n 3 - MDI \n 4 - JOG \n 5 - AUTO \n 6 - Machine Connection \n ')
        print('Select: ')
        mode = msvcrt.getch().decode('utf-8').lower()
        os.system('cls')
        if mode == '1':
            Functions.refMachine()
        if mode == '2':
            Functions.WCS_set()
        if mode == '3':
            Functions.MDI()
        if mode == '4':
            Functions.JOG()
        if mode == '5':
            Functions.AUTO()
        if mode == '6':
            machine.connection()
            
        
        mode = 0 
        
        
Configurator.loadConfig()
while 1:
    mainMenu()
