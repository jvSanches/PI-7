# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 10:17:07 2016

@author: Sanches
"""
import re

def refine(prog):
    ''' breaks a program into lists of lists of strings'''
    # refined_prog = []
    # for line in prog:
    #     no_comments = re.sub(r'\([^()]*\)', '', line)
    #     refined_prog.append(no_comments.split())
    # return refined_prog
    return [re.sub(r'\([^()]*\)', '', line).split() for line in prog]


def parse(prog):
    prog = refine(prog)
    coords = []
    for line in prog:
        coord_line = [0, 0, 0]
        for instruction in line:
            func = instruction[0]
            value = int(instruction[1:])
            if func == 'M' and value == 30:
                return coords

            if func == 'X':
                coord_line[0] = value
            if func == 'Y':
                coord_line[1] = value
            if func == 'Z':
                coord_line[2] = value

        coords.append(coord_line)

    return coords

