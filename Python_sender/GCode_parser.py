# -*- coding: utf-8 -*-
"""
Interpretador de Gcode simplificado
"""
import re

def refine(prog):
    ''' breaks a program into lists of lists of strings'''
    refined_prog = []
    prog = prog.split("\n")
    for line in prog:
        no_comments = re.sub(r'\([^()]*\)', '', line).upper()
        refined_prog.append(no_comments.split())
    return refined_prog
    #return [re.sub(r'\([^()]*\)', '', line).split(" ") for line in prog]

last_x = 2048
last_y = 2048
last_z = 1


def parse(prog):
    global last_x
    global last_y
    global last_z
    prog = refine(prog)
    coords = []
    for line in prog:
        x = None
        y = None
        z = None
        for instruction in line:
            func = instruction[0]
            value = int(float(instruction[1:])*10) 
            if func == 'M' and value == 30:
                return coords

            if func == 'X':
                x = value + 2048
            if func == 'Y':
                y = value + 2048
            if func == 'Z':
                z = value

        if x == None:
            x = last_x
        if y == None:
            y = last_y
        if z == None:
            z = last_z

        last_x, last_y, last_z = x, y, z
        coords.append([x,y,z])

    return coords
