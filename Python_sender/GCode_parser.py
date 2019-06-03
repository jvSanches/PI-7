# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 10:17:07 2016

@author: Sanches
"""
import re

def refine(prog):
    ''' breaks a program into lists of lists of strings'''
    refined_prog = []
    prog = prog.split("\n")
    for line in prog:
        no_comments = re.sub(r'\([^()]*\)', '', line)
        refined_prog.append(no_comments.split())
    return refined_prog
    #return [re.sub(r'\([^()]*\)', '', line).split(" ") for line in prog]

last_x = 0
last_y = 0
last_z = 0


def parse(prog):
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
                x = value
            if func == 'Y':
                y = value
            if func == 'Z':
                z = value

        if not x:
            x = last_x
        if not y:
            y = last_y
        if not z:
            z = last_z

        last_x, last_y, last_z = x, y, z
        coords.append([x,y,z])

    return coords
