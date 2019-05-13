import time
from tkinter import*
import serial
from tkinter import filedialog

import prog_mananger



connection_state = False

xpos,ypos,zpos = 0,0,0

loaded_prog=[]

m1_stop = False

def doConnection():
    global connection_state
    if not connection_state:
        try:
            #print('elooo')
            global machine
            machine = serial.Serial( port_entry.get() ,115200)
            
            port_entry.config(state = 'disabled')
            con_status.config(text = 'Machine Connected', fg= 'green')
            connect.config(text = 'Disconnect')
            connection_state = True
            root.protocol('WM_DELETE_WINDOW')
        except:
            pass
    else:
        machine.close()
        port_entry.config(state = 'normal')
        con_status.config(text = 'Machine not Connected', fg = 'red')
        connect.config(text = 'Connect')
        connection_state = False
        root.protocol('WM_DELETE_WINDOW', root.destroy)
        


def updateTime():
    global machine
    global xpos
    upperframe.after(10, updateTime)
    dateAndTime.config(text = '%s' %(time.ctime()))
    if connection_state:
       if machine.in_waiting != 0:
           xval.config(text = '%.3f' %(float(arduino.readline())) )
          
      
  
def xMeasure():
    pass    
 
  
def yMeasure():
    pass    
 
  
def zMeasure():
    pass    

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
    MDI_Prog = [MDI_input.get()]
    MDI_input.delete(0,END)
    prog_mananger.read(MDI_Prog)
    

def cycleStart():
    act_prog = prog_show.get("0.0", END)
    list_prog = []
    buffer = ''
    for i in act_prog:
        if i != '\n':
            buffer += i
        else:
            list_prog.append(buffer)
            buffer = ''
    prog_mananger.read(list_prog)
    

def reset():
    pass

def m1Stop():
    global m1_stop
    if m1_stop:
        m1_stop = False
        m1stop.config(text = 'Enable M1 Stop')
    else:
        m1stop.config(text = 'Disable M1 Stop')
        m1_stop = True
def REF():
    pass
    
    
    
    
    
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
updateTime()


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

g56_button = Radiobutton(wcs_buttons, command = enableMeasures,  text="G55", variable=selected_wcs, value=3, bg=  'black', fg  = 'white',indicatoron = 0, selectcolor= 'gray', padx = 6)
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
jogzpositive = Button(jogframe, text = 'Z+', font = 'verdana 12 bold ')
jogzpositive.grid(row=2,column =0)
jogznegative = Button(jogframe, text = 'Z-', font = 'verdana 12 bold ')
jogznegative.grid(row=4,column =0)

jogxpositive = Button(jogframe, text = 'X+', font = 'verdana 12 bold ')
jogxpositive.grid(row=3,column =3)
jogxnegative = Button(jogframe, text = 'X-', font = 'verdana 12 bold ')
jogxnegative.grid(row=3,column =1)

jogypositive = Button(jogframe, text = 'Y+', font = 'verdana 12 bold ')
jogypositive.grid(row=2,column =2)
jogynegative = Button(jogframe, text = 'Y-', font = 'verdana 12 bold ')
jogynegative.grid(row=4,column =2)

jogstepselector = Frame(jogframe, borderwidth = 10, bg = 'black' )
jogstepselector.grid(row = 5, column = 0, columnspan = 5)

Label(jogstepselector, text = 'Jog Step:', bg= 'black', fg = 'white').pack(side = 'left')
onejog = Radiobutton(jogstepselector, text="1 mm", variable= jog_step, value=1, bg=  'black', fg  = 'white',indicatoron =0, selectcolor= 'gray', padx = 6).pack(side = 'left' )
eithjog =  Radiobutton(jogstepselector, text="0.25 mm", variable= jog_step, value=8, bg=  'black', fg  = 'white',indicatoron =0, selectcolor= 'gray', padx = 6).pack(side = 'left' )
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





root.mainloop()