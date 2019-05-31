# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 18:48:01 2016

@author: Sanches
"""
import machine
import math
#from matplotlib import pyplot
#import pylab
#from mpl_toolkits.mplot3d import Axes3D


machine_step= machine.machine_step= 1/40961/4096
accuracy = machine_step / 3



def approachCoordinate(n):
    steps = n // machine_step
    n_app = machine_step * steps    
    if round((n - n_app),8) < (machine_step/2):        
        return round(n_app,8)
    else:
        return round (n_app + machine_step,8)
        
def dist(point_a,point_b):
    dist2 = (point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2\
    + (point_a[2]-point_b[2])**2
    
    return( math.sqrt(dist2))

        
def refinePoints(curve_points):
    refined_points = refined_points_2= []    
    if len(curve_points) != 0:
    
        refined_points.append(curve_points[0])
        for i in range(len(curve_points)):
            if refined_points[-1]!= curve_points[i]:
                refined_points.append(curve_points[i])
                #print(refined_points[-1])
        
        refined_points_2=[refined_points[0]]
        
       
        pos = 0    
        o = 2
        over = False
        #print(refined_points_2)
        min_dist = 1
        while not over: #pos < len(refined_points)and 
            dist_to_end = round(dist(refined_points[-1],refined_points[pos]),8)             
            #print(dist_to_end)
            
            if dist_to_end <= round(machine_step * math.sqrt(3) , 8):
               
                over = True
                refined_points_2.append(refined_points[-1])
            
            
            elif dist(refined_points[pos], refined_points[pos + o]) > machine_step * math.sqrt(3):
                pos = pos + o - 1            
                refined_points_2.append(refined_points[pos])
                o = 2
                
            else: 
                o += 1
            
            if dist_to_end < 0.01:
                #print('aqui',min_dist)
                if min_dist > dist_to_end - 0.0000000001:
                    min_dist = dist_to_end
                    
                else:
                    mid_point = [approachCoordinate((refined_points[-1][0] + refined_points[pos][0])/2),\
                    approachCoordinate((refined_points[-1][1] + refined_points[pos][1])/2),\
                    approachCoordinate((refined_points[-1][2] + refined_points[pos][2])/2)]
                    refined_points_2.append(mid_point)
                    refined_points_2.append(refined_points[-1])
                    over = True
            
        
            
        
            
    return refined_points_2 
        





        
def getAngle(vector):
    if vector[0] > 0 :
        a = vector[1]/vector[0]
        if a>= 0 :
            
            return math.atan(a)
        else:
            return (2*math.pi+math.atan(a))
    elif vector[0] == 0 :
        if vector[1] > 0:
            return ( math.pi / 2)
        else:
            return (3* math.pi / 2 )
    else:
        a = vector[1]/vector[0]
        return (math.pi + math.atan(a))        
        
        
        
def getSteps(points):
    to_step=[]    
    for i in range(1,len(points)):
        to_step.append([int(round((points[i][0]-points[i-1][0])/machine_step)),\
        int(round((points[i][1]-points[i-1][1])/machine_step)),\
        int(round((points[i][2]-points[i-1][2])/machine_step))])
        #print(to_step[-1])
    
    return to_step
    
                
        
        
        
        
def generate_move(curve_type, dest_x, dest_y, dest_z, i=0, j=0, k=0):
    '''gives the list of steps to take'''
        
    if curve_type == 0 or curve_type == 1:
        
        dx = dest_x - machine.machine_pos[0]
        dy = dest_y - machine.machine_pos[1]
        dz = dest_z - machine.machine_pos[2]
        
        curve_len = math.sqrt(dx**2+dy**2+dz**2)*1.01 + 0.01
        
        curve_points=[]
        
        a = accuracy
        
        #print(curve_len,dest_z)
        while a <= curve_len:
            t = a / curve_len
            curve_points.append([approachCoordinate(t*dx),\
            approachCoordinate(t*dy), approachCoordinate(t*dz)])
            a += accuracy
           
        #print(curve_points) 
        refined_points = refinePoints(curve_points)
        
        return getSteps(refined_points)
            
    if curve_type == 2 or curve_type == 3:
        curve_points=[]
        
        a = accuracy
        
        dz = dest_z - machine.machine_pos[2]
        
        center_point = [round(machine.machine_pos[0],3)+i,\
        round(machine.machine_pos[1],3)+ j,round(machine.machine_pos[2],3)+ k]
        
        start_vec = machine.machine_pos[0]-center_point[0],\
        machine.machine_pos[1]-center_point[1],\
        machine.machine_pos[2]-center_point[2]
        
        end_vec = dest_x - center_point[0],\
        dest_y - center_point[1],\
        dest_z - center_point[2]
        
        start_ang = getAngle(start_vec)
        end_ang = getAngle(end_vec)
        
        
        if curve_type == 3 and end_ang < start_ang:
            end_ang += 2* math.pi
            
        
        R_start = math.sqrt(start_vec[0]**2+start_vec[1]**2) 
        R_end = math.sqrt(end_vec[0]**2+end_vec[1]**2)
        
        R = R_start 
        
        curve_len = (abs(end_ang-start_ang) * R)*1.01 + 0.01
         
        #print(start_ang,end_ang, curve_len)
        direction = 1        
        
        if curve_type == 2:
            direction = -1
        
        t = direction * accuracy / R
       
        n = 0      
        
        while a < (curve_len ):            
            curve_points.append([approachCoordinate(center_point[0] + (R * math.cos(start_ang + n * t))),\
            approachCoordinate(center_point[1] + (R * math.sin(start_ang + n * t))),\
            approachCoordinate(machine.machine_pos[2] + dz *( a / curve_len))])
            a += accuracy
            n += 1 
            
            #print(curve_points[-1],'aa')
            
        
    
        curve_points.append([dest_x,dest_y,dest_z])    
        #return curve_points
        refined_points = refinePoints(curve_points)
        
        return (getSteps(refined_points))
        
        
               
        
        
        
'''        
def getMoveList():
    move_list = generate_move(0,1,-20,1)    
    
    steps_ = getSteps(move_list)
    
    #fig = pylab.figure()
    #ax = Axes3D(fig)
    
    #for u in range(len(lista)-1):
        
    #    ax.scatter(lista[u][0],lista[u][1],lista[u][2])
    #    print(lista[u])
    #    print(steps_[u])
    #pyplot.show()
    
    return steps_
            
'''

        
        