import time
from tkinter import*
import serial
from tkinter import filedialog
import machine
import prog_mananger
import struct


connection_state = False

xpos, ypos, zpos = 0, 0, 0
xstep, ystep, zstep = 4, 4, 4
act_s = 0
act_f =  15
loaded_prog = []

m1_stop = False
def readReport(report):
    global xpos, ypos, zpos, act_f, act_s
    next_space = report.index(' ')
    xpos = float(report[0:next_space])
    report = report[next_space +1 :]
    next_space = report.index(' ')
    ypos = float(report[0:next_space])
    report = report[next_space+1 :]
    next_space = report.index(' ')
    zpos = float(report[0:next_space])
    report = report[next_space+1:]
    next_space = report.index(' ')
    xstep = int(report[0:next_space])
    report = report[next_space+1:]
    next_space = report.index(' ')
    ystep = int(report[0:next_space])
    report = report[next_space+1:]
    next_space = report.index(' ')
    zstep = int(report[0:next_space])
    report = report[next_space+1:]
    next_space = report.index(' ')
    act_f = int(report[0:next_space])
    report = report[next_space+1:]
    next_space = report.index(' ')
    act_s = int(report[0:next_space])
    report = report[next_space+1:]
    machine.standingBy = bool(int(report))
    
    
    

    machine.machine_pos =[xpos, ypos, zpos ]
    machine.machine_steps =[xstep, ystep, zstep ]
    machine.saveData()
    selec = int(selected_wcs.get())
    
    if selec == 1:
        xpos -= machine.G54[0]
        ypos -= machine.G54[1]
        zpos -= machine.G54[2]
    elif selec == 2:
        xpos -= machine.G55[0]
        ypos -= machine.G55[1]
        zpos -= machine.G55[2]
    elif selec == 3:
        xpos -= machine.G56[0]
        ypos -= machine.G56[1]
        zpos -= machine.G56[2]


def doConnection():
    global connection_state
    if not connection_state:
        try:
            #print('elooo')
            global mymachine
            mymachine = serial.Serial(port_entry.get(), 115200)
            port_entry.config(state ='disabled')
            con_status.config(text = 'Machine Connected', fg= 'green')
            connect.config(text = 'Disconnect')
            connection_state = True
            root.protocol('WM_DELETE_WINDOW')
            machine.mymachine = mymachine
        except:
            pass
    else:
        mymachine.close()
        port_entry.config(state = 'normal')
        con_status.config(text = 'Machine not Connected', fg = 'red')
        connect.config(text = 'Connect')
        connection_state = False
        root.protocol('WM_DELETE_WINDOW', root.destroy)
        
def readSerial():
    global root , mymachine, act_f, act_s
    dateAndTime.config(text = '%s' %(time.ctime()))
    
    if connection_state:
        if mymachine.in_waiting != 0:
            buffer = str(mymachine.readline())[2:-5]
            if buffer[0]== '1' :
                readReport(buffer[2:])
                
        xval.config(text = '%.3f' %(xpos))
        yval.config(text = '%.3f' %(ypos))
        zval.config(text = '%.3f' %(zpos))
        activeFEEDlabel.config(text = '%d' % (act_f))
        activeRPMlabel.config(text = '%d' %(act_s))

def refresh(lin):
    new_lin=''
    for a in ['x','y', 'z']:
        if a in lin:            
            index = lin.index(a)
            new_lin = lin[:index]
            value = machine.machine_pos(ord(a)-120) 
            
            new_lin += str(value)
            new_lin += lin[index+1:]

            lin = new_lin
    return lin




def doThings(buffer):
    if machine.standingBy:
        if buffer != []:
            machine.standingBy = False
            line = buffer.pop(0)
            if line[2] ==2:
                line = line.refresh()
            mymachine.write(line)



def updateTime():
    global mymachine, act_f, act_s
    
    root.after(10, updateTime)
    
    readSerial()

    doThings(machine.out_buffer)
    #if mymachine.in_waiting != 0:
    #         buffer = str(mymachine.readline())[2:-5]
    #         if buffer[0]== '1' :
    #             readReport(buffer[2:])
    # xval.config(text = '%.3f' %(xpos))
    # yval.config(text = '%.3f' %(ypos))
    # zval.config(text = '%.3f' %(zpos))
    # activeFEEDlabel.config(text = '%d' % (act_f))
    # activeRPMlabel.config(text = '%d' %(act_s))
    
  
def xMeasure():
    offset = xwcs_entry.get()
    if offset == '':
        return
    offset=float(offset)
    selec = int(selected_wcs.get())
    
    if selec ==1:
        machine.G54[0] = machine.machine_pos[0] - offset
    elif selec ==2:
        machine.G55[0] = machine.machine_pos[0] - offset
    elif selec ==3:
        machine.G56[0] = machine.machine_pos[0] - offset
    xwcs_entry.delete(0, END)
    machine.saveData()
  
def yMeasure():
    offset = ywcs_entry.get()
    if offset == '':
        return
    offset=float(offset)
    selec = int(selected_wcs.get())
    
    if selec ==1:
        machine.G54[1] = machine.machine_pos[1] - offset
    elif selec ==2:
        machine.G55[1] = machine.machine_pos[1] - offset
    elif selec ==3:
        machine.G56[1] = machine.machine_pos[1] - offset
    ywcs_entry.delete(0, END)    
    machine.saveData()
 
  
def zMeasure():
    offset = zwcs_entry.get()
    if offset == '':
        return
    offset=float(offset)
    selec = int(selected_wcs.get())
    
    if selec ==1:
        machine.G54[2] = machine.machine_pos[2] - offset
    elif selec ==2:
        machine.G55[2] = machine.machine_pos[2] - offset
    elif selec ==3:
        machine.G56[2] = machine.machine_pos[2] - offset
    zwcs_entry.delete(0, END)    
    machine.saveData()

def disableMeasures():
    global x_measure, y_measure, z_measure
    x_measure.config(state = 'disabled')
    y_measure.config(state = 'disabled')
    z_measure.config(state = 'disabled')
 
def enableMeasures():
    global x_measure, y_measure, z_measure
    x_measure.config(state = 'normal')
    y_measure.config(state = 'normal')
    z_measure.config(state = 'normal')
    

def jogxmore() :
    if machine.standingBy:
        steptojog = 1/ int(jog_step.get())
        pack_to_send = '2 '
        pack_to_send +=  '0 %.3f %.3f %.3f 0.0 0.0 ' %((machine.machine_pos[0] + steptojog ,machine.machine_pos[1],machine.machine_pos[2]))
        message = bytes(pack_to_send, 'utf-8')
        mymachine.write(message)
        
            

def jogxless():
    if machine.standingBy:
        steptojog = 1/ int(jog_step.get())
        pack_to_send = '2 '
        pack_to_send +=  '0 %.3f %.3f %.3f 0.0 0.0 ' %((machine.machine_pos[0] - steptojog ,machine.machine_pos[1],machine.machine_pos[2]))
        message = bytes(pack_to_send, 'utf-8')
        mymachine.write(message)
def jogymore() :
    if machine.standingBy:
        steptojog = 1/ int(jog_step.get())
        pack_to_send = '2 '
        pack_to_send +=  '0 %.3f %.3f %.3f 0.0 0.0 ' %((machine.machine_pos[0] ,machine.machine_pos[1]+ steptojog ,machine.machine_pos[2]))
        message = bytes(pack_to_send, 'utf-8')
        mymachine.write(message)
        
            

def jogyless():
    if machine.standingBy:
        steptojog = 1/ int(jog_step.get())
        pack_to_send = '2 '
        pack_to_send +=  '0 %.3f %.3f %.3f 0.0 0.0 ' %((machine.machine_pos[0],machine.machine_pos[1] - steptojog ,machine.machine_pos[2]))
        message = bytes(pack_to_send, 'utf-8')
        mymachine.write(message)
def jogzmore() :
    if machine.standingBy:
        steptojog = 1/ int(jog_step.get())
        pack_to_send = '2 '
        pack_to_send +=  '0 %.3f %.3f %.3f 0.0 0.0 ' %((machine.machine_pos[0] ,machine.machine_pos[1],machine.machine_pos[2]+ steptojog ))
        message = bytes(pack_to_send, 'utf-8')
        mymachine.write(message)
        
            

def jogzless():
    if machine.standingBy:
        steptojog = 1/ int(jog_step.get())
        pack_to_send = '2 '
        pack_to_send +=  '0 %.3f %.3f %.3f 0.0 0.0 ' %((machine.machine_pos[0],machine.machine_pos[1]  ,machine.machine_pos[2]- steptojog))
        message = bytes(pack_to_send, 'utf-8')
        mymachine.write(message)


def enableJOG():
    jogzpositive.config(state = 'normal')
    jogznegative.config(state = 'normal')
    jogxpositive.config(state = 'normal')
    jogxnegative.config(state = 'normal')
    jogypositive.config(state = 'normal')
    jogynegative.config(state = 'normal')
    
def disableJOG():
    jogzpositive.config(state = 'disabled')
    jogznegative.config(state = 'disabled')
    jogxpositive.config(state = 'disabled')
    jogxnegative.config(state = 'disabled')
    jogypositive.config(state = 'disabled')
    jogynegative.config(state = 'disabled')
    
def clear():
    global prog_show
    prog_show.delete('0.0',END)
    
    
    
def openFile():
    global prog_show, loaded_prog
    filename = filedialog.askopenfilename()
    try:
        file = open(filename,'r')
        loaded_prog = []
        for i in file:
            loaded_prog.append(i.rstrip())
        for k in range(len(loaded_prog)):
            loaded_prog[k] = loaded_prog[k]#.upper()
        file.close()
    except:
        pass
    prog_show.delete('0.0',END)
    for l in loaded_prog:        
        prog_show.insert(END, l+"\n" )
        
        
def runMDI():
    MDI_Prog = ['n0']
    MDI_Prog.append(MDI_input.get())
    MDI_input.delete(0,END)
    MDI_Prog[1] = MDI_Prog[1].upper()
    # print(MDI_Prog)
    prog_mananger.read(MDI_Prog)
    

def cycleStart():
    act_prog = prog_show.get("0.0", END)
    list_prog = []
    buffer = ''
    for i in act_prog:
        if i != '\n':
            buffer += i
        else:
            list_prog.append(buffer.upper())
            buffer = ''
    print(list_prog)
    prog_mananger.read(list_prog)
    

def reset():
    message = bytes('9', 'utf-8')
    mymachine.write(message)
    machine.out_buffer = []
    

def m1Stop():
    global m1_stop
    if m1_stop:
        m1_stop = False
        m1stop.config(text = 'Enable M1 Stop')
    else:
        m1stop.config(text = 'Disable M1 Stop')
        m1_stop = True
def REF():
    machine.loadData()
    pack_to_send = '1 ' + str(machine.machine_pos[0]) + ' ' +  str(machine.machine_pos[1]) + ' '+ str(machine.machine_pos[2]) + ' '
    pack_to_send += str(machine.machine_steps[0]) + ' ' +  str(machine.machine_steps[1]) + ' '+ str(machine.machine_steps[2])
    message = bytes(pack_to_send, 'utf-8')
    mymachine.write(message)
    
    
    
    
    
    
root = Tk()
jog_step = IntVar()
jog_step.set(1)  
selected_wcs = IntVar()
selected_wcs.set(0)   
root.title('M^4 Control Panel')
root.resizable(width=False, height=False)
upperframe = Frame(root, bg = 'black')
upperframe.pack(side= 'top')
logo = Label(upperframe, text ='CNC', fg = 'blue', bg = 'black',\
             font = "Times 50 bold  ", width = 5)

logo.pack(side = 'left')
Frame(upperframe, bg= 'white', width = 5).pack(fill = 'y', side = 'left')

clock = Frame(upperframe, bg = 'black')
clock.pack(side = 'left')
dateAndTime= Label(clock, bg = 'black', fg = 'white' , text = '%s' %(time.ctime()), font = 'verdana 12 bold', width = 40)
dateAndTime.grid(row = 0)



Frame(upperframe, bg= 'white', width = 5).pack(fill = 'y', side = 'left')



connection = Frame(upperframe, bg = 'black', borderwidth = 10)
connection.pack(side = 'right')
con_port = Label(connection, text = 'Port to Connect:', fg = 'white', bg = 'black')
con_port.grid(row = 0, column =0, sticky = 'e' )
port_entry = Entry(connection)
port_entry.grid(row = 0, column = 1)
con_status = Label(connection, text = 'Machine not Connected', fg = 'red', bg = 'black')
con_status.grid(row =1 , column =0, sticky = 'e' )
connection.columnconfigure(0, minsize = 150)
connect = Button(connection, text = 'Connect', bg= 'light gray', command = doConnection)
connect.grid(row = 1, column = 1)

Frame(root, bg= 'white', height = 5).pack(fill = 'x', side = 'top')


#segunda linha
midframe = Frame(root,bg = 'black')
midframe.pack(side = 'top', fill = 'x')
positions = Frame(midframe, bg = 'black' , height = 300, borderwidth = 10)
positions.pack(side= 'left')
positions.columnconfigure(0, minsize = 60)

positiontitle = Label(positions, bg ='black', text = 'Position', font = 'verdana 15', fg = 'white')
positiontitle.grid(row = 0, columnspan = 2)
xlabel = Label(positions, bg ='black', text = 'X:', font = 'verdana 30', fg = 'white')
xlabel.grid(row = 1 , column = 0)

ylabel = Label(positions, bg ='black', text = 'Y:', font = 'verdana 30', fg = 'white')
ylabel.grid(row = 2 , column = 0)

zlabel = Label(positions, bg ='black', text = 'Z:', font = 'verdana 30', fg = 'white')
zlabel.grid(row = 3 , column = 0)

positions.columnconfigure(1, minsize = 200)
xval= Label(positions, bg ='black', text = '%.3f' %(xpos), font = 'verdana 30', fg = 'white', anchor = 'e', justify = 'right')
xval.grid(row = 1 , column = 1,sticky = 'e')

yval = Label(positions, bg ='black', text = '%.3f' %(ypos), font = 'verdana 30', fg = 'white', anchor = 'e', justify = 'right')
yval.grid(row = 2 , column = 1, sticky = 'e')

zval = Label(positions, bg ='black', text = '%.3f' %(zpos), font = 'verdana 30', fg = 'white', anchor = 'e', justify = 'right')
zval.grid(row = 3 , column = 1,sticky = 'e')

Frame(positions, bg= 'white', width = 2, height = 200).grid(row = 0 ,column =2, rowspan = 4, sticky = 'n' )
#positions.columnconfigure(2, minsize = 5)

#wcss = Frame(midframe, bg = 'black' , borderwidth = 10)
#wcss.pack(side= 'left', fill = 'y')

positiontitle = Label(positions, bg ='black', text = 'WCS:', font = 'verdana 10', fg = 'white')
positiontitle.grid(row = 0, column = 3)
#
xwcs = Label(positions, bg ='black', text = 'X:', font = 'verdana 15', fg = 'white')
xwcs.grid(row = 1 , column = 3)
positions.columnconfigure(3, minsize = 60)

ywcs = Label(positions, bg ='black', text = 'Y:', font = 'verdana 15', fg = 'white')
ywcs.grid(row = 2 , column = 3)

zwcs = Label(positions, bg ='black', text = 'Z:', font = 'verdana 15', fg = 'white')
zwcs.grid(row = 3 , column = 3)

xwcs_entry = Entry(positions)
xwcs_entry.grid(row = 1, column = 4)

ywcs_entry = Entry(positions)
ywcs_entry.grid(row = 2, column = 4)

zwcs_entry = Entry(positions)
zwcs_entry.grid(row = 3, column = 4)

wcs_buttons = Frame(positions, bg = 'black' )
wcs_buttons.grid(row =0 , column = 4)
g53_button = Radiobutton(wcs_buttons,command = disableMeasures,text="G53", variable=selected_wcs, value=0, bg=  'black', fg  = 'white',indicatoron =0, selectcolor= 'gray', padx = 6)
g53_button.pack(side = 'left')

g54_button = Radiobutton(wcs_buttons, command = enableMeasures, text="G54", variable=selected_wcs, value=1, bg=  'black', fg  = 'white',indicatoron =0, selectcolor= 'gray', padx = 6)
g54_button.pack(side = 'left')

g55_button = Radiobutton(wcs_buttons,command = enableMeasures, text="G55", variable=selected_wcs, value=2, bg=  'black', fg  = 'white',indicatoron = 0, selectcolor= 'gray', padx = 6)
g55_button.pack(side = 'left')

g56_button = Radiobutton(wcs_buttons, command = enableMeasures,  text="G56", variable=selected_wcs, value=3, bg=  'black', fg  = 'white',indicatoron = 0, selectcolor= 'gray', padx = 6)
g56_button.pack(side = 'left')

positions.columnconfigure(5, minsize =80)

x_measure = Button(positions, text ='Measure', command = xMeasure)
x_measure.grid(row = 1, column = 5)

y_measure = Button(positions, text ='Measure', command = yMeasure)
y_measure.grid(row = 2, column = 5)

z_measure = Button(positions, text ='Measure', command = zMeasure)
z_measure.grid(row = 3, column = 5)

disableMeasures()

Frame(positions, bg= 'white', width = 2, height = 200).grid(row = 0 ,column =6, rowspan = 4, sticky = 'n' )
#### ultima posicao do meio

Frame(root, bg= 'white', height = 5).pack(fill = 'x', side = 'top')

jogframe = Frame(midframe, bg = 'black', borderwidth = 10)
jogframe.pack(side ='left', fill = 'both')

enable_jog = Button(jogframe, text= 'Enable JOG', command = enableJOG)
enable_jog.grid(row = 0, column = 0, sticky = 'N')
disable_jog = Button(jogframe, text= 'Disable JOG', command = disableJOG)
disable_jog.grid(row = 0, column = 4, sticky = 'N')

jogframe.rowconfigure(1, minsize = 20)
jogzpositive = Button(jogframe, text = 'Z+', font = 'verdana 12 bold ', command = jogzmore)
jogzpositive.grid(row=2,column =0)
jogznegative = Button(jogframe, text = 'Z-', font = 'verdana 12 bold ', command = jogzless)
jogznegative.grid(row=4,column =0)

jogxpositive = Button(jogframe, text = 'X+', font = 'verdana 12 bold ', command = jogxmore)
jogxpositive.grid(row=3,column =3)
jogxnegative = Button(jogframe, text = 'X-', font = 'verdana 12 bold ', command = jogxless)
jogxnegative.grid(row=3,column =1)

jogypositive = Button(jogframe, text = 'Y+', font = 'verdana 12 bold ', command = jogymore)
jogypositive.grid(row=2,column =2)
jogynegative = Button(jogframe, text = 'Y-', font = 'verdana 12 bold ', command = jogyless)
jogynegative.grid(row=4,column =2)

jogstepselector = Frame(jogframe, borderwidth = 10, bg = 'black' )
jogstepselector.grid(row = 5, column = 0, columnspan = 5)

Label(jogstepselector, text = 'Jog Step:', bg= 'black', fg = 'white').pack(side = 'left')
onejog = Radiobutton(jogstepselector, text="1 mm", variable= jog_step, value=1, bg=  'black', fg  = 'white',indicatoron =0, selectcolor= 'gray', padx = 6).pack(side = 'left' )
eithjog =  Radiobutton(jogstepselector, text="0.25 mm", variable= jog_step, value=4, bg=  'black', fg  = 'white',indicatoron =0, selectcolor= 'gray', padx = 6).pack(side = 'left' )
centjog =  Radiobutton(jogstepselector, text="0.015 mm", variable= jog_step, value=64, bg=  'black', fg  = 'white',indicatoron =0, selectcolor= 'gray', padx = 6).pack(side = 'left' )
milijog =  Radiobutton(jogstepselector, text="0.001 mm", variable= jog_step, value=1024 ,bg=  'black', fg  = 'white',indicatoron =0, selectcolor= 'gray', padx = 6).pack(side = 'left' )
disableJOG()

lowerframe = Frame(root,bg='black', height = 300)
lowerframe.pack(fill = 'x')

speedscontrol = Frame(lowerframe, borderwidth = 10, bg = 'black')
speedscontrol.pack(side = 'left')
speedscontrol.rowconfigure(0, minsize = 40)
Label(speedscontrol, bg = 'black', fg  = 'white' ,text = 'Feed and Speeds:', font = 15).grid(row = 0,sticky = 'n', column = 0, columnspan = 2)
Label(speedscontrol, bg = 'black', fg  = 'white' ,text = 'Prg. RPM:').grid(row = 1, column = 0)
RPMlabel = Label(speedscontrol, bg = 'black', fg  = 'white', text = '0')
RPMlabel.grid(row = 1, column = 1)

RPM = Scale(speedscontrol, from_=20, to=150, orient=HORIZONTAL, bg= 'black', fg = 'white', length= 200)
RPM.set(100)
RPM.grid(row = 2, column = 0, columnspan = 2 )

Label(speedscontrol, bg = 'black', fg  = 'white' ,text = 'Act. RPM:').grid(row = 3, column = 0)
activeRPMlabel = Label(speedscontrol, bg = 'black', fg  = 'white', text = '0')
activeRPMlabel.grid(row = 3, column = 1)


Label(speedscontrol, bg = 'black', fg  = 'white' ,text = 'Prg. FEED:').grid(row = 4, column = 0)
FEEDlabel = Label(speedscontrol, bg = 'black', fg  = 'white', text = '0')
FEEDlabel.grid(row = 4, column = 1)

FEED = Scale(speedscontrol, from_=0, to=120, orient=HORIZONTAL, bg= 'black', fg = 'white', length= 200)
FEED.set(100)
FEED.grid(row = 5, column = 0, columnspan = 2 )
Label(speedscontrol, bg = 'black', fg  = 'white' ,text = 'Act. FEED:').grid(row = 6, column = 0)

activeFEEDlabel = Label(speedscontrol, bg = 'black', fg  = 'white', text = '0')
activeFEEDlabel.grid(row = 6, column = 1)

Frame(lowerframe, bg= 'white', width = 2, height = 220, pady = 10).pack(side = 'left')

progframe = Frame(lowerframe, bg = 'black', borderwidth = 10);
progframe.pack(side = 'left', fill = 'y')


MDI_frame = Frame(progframe, borderwidth = 3, bg = 'black')
MDI_frame.pack(side = 'bottom')
MDI_input = Entry(MDI_frame, width =80, borderwidth = 2)
MDI_input.pack(side= 'left', fill = 'y')
MDI_button = Button(MDI_frame, text = 'Run MDI', command = runMDI)
MDI_button.pack(side = 'left')


Frame(lowerframe, bg= 'white', width = 2, height = 220, pady = 10).pack(side = 'left')

scrollbar = Scrollbar(progframe)
prog_show  = Text(progframe , height= 10, width = 52, font = 'verdana 12')
scrollbar.pack(side = 'right', fill = 'y')
prog_show.pack(side = 'top')
scrollbar.config(command=prog_show.yview)
prog_show.config(yscrollcommand=scrollbar.set)

optionsframe = Frame(lowerframe, bg = 'black', borderwidth = 10)
optionsframe.pack(side = 'left')

cy_start = Button(optionsframe, text = 'Cycle Start', command= cycleStart, width = 20)
cy_start.pack(side = 'top')
Label(optionsframe, bg = 'black', height = 1).pack()
rst = Button(optionsframe, text = 'Reset', command = reset, width = 20)
rst.pack()
Label(optionsframe, bg = 'black', height = 1).pack()

m1stop = Button(optionsframe, text = 'Enable M1 Stop', command= m1Stop, width = 20)
m1stop.pack()
Label(optionsframe, bg = 'black', height = 1).pack()
ref_buttom = Button(optionsframe, text = 'REF machine', command = REF)
ref_buttom.pack()
Label(optionsframe, bg = 'black', height = 1).pack()

browse_button = Button(optionsframe, text = 'Open File', command = openFile, width = 10)
browse_button.pack(side = 'left')

rld_button = Button(optionsframe, text = 'Clear', command = clear, width = 8)
rld_button.pack(side = 'right')
updateTime()





root.mainloop()