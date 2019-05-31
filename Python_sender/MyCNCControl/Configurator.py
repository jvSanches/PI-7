# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 17:19:06 2017

@author: Sanches
"""
import machine


def loadConfig():
    POS_file = open('C:\\Users\\Sanches\\Documents\\My CNC\\M^4\\OS\\Settings\\POS','r')
    machine.machine_pos[0] = float(POS_file.readline())
    machine.machine_pos[1] = float(POS_file.readline())
    machine.machine_pos[2] = float(POS_file.readline())
    POS_file.close()
    
    G53_file = open('C:\\Users\\Sanches\\Documents\\My CNC\\M^4\\OS\\Settings\\G53','r')
    machine.G53[0] = float(G53_file.readline())
    machine.G53[1] = float(G53_file.readline())
    machine.G53[2] = float(G53_file.readline())
    G53_file.close()
    
    G54_file = open('C:\\Users\\Sanches\\Documents\\My CNC\\M^4\\OS\\Settings\\G54','r')
    machine.G54[0] = float(G54_file.readline())
    machine.G54[1] = float(G54_file.readline())
    machine.G54[2] = float(G54_file.readline())
    G54_file.close()
    
    G55_file = open('C:\\Users\\Sanches\\Documents\\My CNC\\M^4\\OS\\Settings\\G55','r')
    machine.G55[0] = float(G55_file.readline())
    machine.G55[1] = float(G55_file.readline())
    machine.G55[2] = float(G55_file.readline())
    G55_file.close()
    
    G56_file = open('C:\\Users\\Sanches\\Documents\\My CNC\\M^4\\OS\\Settings\\G56','r')
    machine.G56[0] = float(G56_file.readline())
    machine.G56[1] = float(G56_file.readline())
    machine.G56[2] = float(G56_file.readline())
    G56_file.close()
    
def savePos():
    POS_file = open('C:\\Users\\Sanches\\Documents\\My CNC\\M^4\\OS\\Settings\\POS','w')
    POS_file.write(str(machine.machine_pos[0]))
    POS_file.write('\n')
    POS_file.write(str(machine.machine_pos[1]))
    POS_file.write('\n')
    POS_file.write(str(machine.machine_pos[2]))
    POS_file.write('\n')
    POS_file.close()

def saveConfig():
    G53_file = open('C:\\Users\\Sanches\\Documents\\My CNC\\M^4\\OS\\Settings\\G53','w')
    G53_file.write(str(machine.G53[0]))
    G53_file.write('\n')
    G53_file.write(str(machine.G53[1]))
    G53_file.write('\n')
    G53_file.write(str(machine.G53[2]))
    G53_file.write('\n')
    G53_file.close()
    
    G54_file = open('C:\\Users\\Sanches\\Documents\\My CNC\\M^4\\OS\\Settings\\G54','w')
    G54_file.write(str(machine.G54[0]))
    G54_file.write('\n')
    G54_file.write(str(machine.G54[1]))
    G54_file.write('\n')
    G54_file.write(str(machine.G54[2]))
    G54_file.write('\n')
    G54_file.close()
    
    G55_file = open('C:\\Users\\Sanches\\Documents\\My CNC\\M^4\\OS\\Settings\\G55','w')
    G55_file.write(str(machine.G55[0]))
    G55_file.write('\n')
    G55_file.write(str(machine.G55[1]))
    G55_file.write('\n')
    G55_file.write(str(machine.G55[2]))
    G55_file.write('\n')
    G55_file.close()
    
    G56_file = open('C:\\Users\\Sanches\\Documents\\My CNC\\M^4\\OS\\Settings\\G56','w')
    G56_file.write(str(machine.G56[0]))
    G56_file.write('\n')
    G56_file.write(str(machine.G56[1]))
    G56_file.write('\n')
    G56_file.write(str(machine.G56[2]))
    G56_file.write('\n')
    G56_file.close()
 