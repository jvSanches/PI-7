import time
from tkinter import*
from tkinter import filedialog
import struct

import GCode_parser
import modbus_sender

connection_state = False

xpos, ypos, zpos, line = 0, 0, 0, 0
x_offset, y_offset = 0, 0
loaded_prog = []

m1_stop = False


def doConnection():
    global connection_state
    if not connection_state:
        modbus_sender.LPC_connect(port_entry.get())
        port_entry.config(state ='disabled')
        con_status.config(text = 'Machine Connected', fg= 'green')
        connect.config(text = 'Disconnect')
        #root.protocol('WM_DELETE_WINDOW')
        connection_state = True
    else:
        modbus_sender.LPC_disconnect()
        port_entry.config(state = 'normal')
        con_status.config(text = 'Machine not Connected', fg = 'red')
        connect.config(text = 'Connect')
        connection_state = False
        #root.protocol('WM_DELETE_WINDOW', root.destroy)

def readSerial():
    global root
    dateAndTime.config(text = '%s' %(time.ctime()))

    if connection_state:
        xpos = modbus_sender.ReadRegister(1,0)
        ypos = modbus_sender.ReadRegister(1,1)
        zpos = modbus_sender.ReadRegister(1,2)
        line = modbus_sender.ReadRegister(1,3)

        xval.config(text = '%.3f' %(xpos-x_offset))
        yval.config(text = '%.3f' %(ypos-y_offset))
        zval.config(text = '%.3f' %(zpos))
        lineval.config(text = '%d' %(line))

def updateTime():
    root.after(100, updateTime)

    #readSerial()

def disableMeasures():
    global x_measure, y_measure
    x_measure.config(state = 'disabled')
    y_measure.config(state = 'disabled')

def enableMeasures():
    global x_measure, y_measure
    x_measure.config(state = 'normal')
    y_measure.config(state = 'normal')

def measureX():
    x_pos = x_offset = modbus_sender.ReadRegister(1,0)

def measureY():
    y_pos = y_offset = modbus_sender.ReadRegister(1,1)

def jogxmore() :
    modbus_sender.WriteSingleRegister(1,4,1)

def jogxless():
    modbus_sender.WriteSingleRegister(1,5,1)

def jogymore():
    modbus_sender.WriteSingleRegister(1,6,1)

def jogyless():
    modbus_sender.WriteSingleRegister(1,7,1)

def jogzmore():
    modbus_sender.WriteSingleRegister(1,8,1)

def jogzless():
    modbus_sender.WriteSingleRegister(1,8,0)

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

def sendFile():
    global loaded_prog
    loaded_prog = prog_show.get("1.0", "end-1c")
    coords = GCode_parser.parse(loaded_prog)
    print(coords)
    coords = [[line[0]+x_offset, line[1]+y_offset, line[2]] for line in coords]
    modbus_sender.WriteSingleRegister(1,10,0)
    modbus_sender.sendLines(1, coords)


def start():
    disableJOG()
    modbus_sender.WriteSingleRegister(1,0,1)


def stop():
    enableJOG()
    modbus_sender.WriteSingleRegister(1,1,1)


def REF():
    modbus_sender.WriteSingleRegister(1,9,1)


root = Tk()

root.title('PI7 Controller')
root.resizable(width=False, height=False)
upperframe = Frame(root, bg = 'black')
upperframe.pack(side= 'top')
logo = Label(upperframe, text ='PI-7', fg = 'blue', bg = 'black',\
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

linelabel = Label(positions, bg ='black', text = 'Line:', font = 'verdana 30', fg = 'white')
linelabel.grid(row = 4 , column = 0)

positions.columnconfigure(1, minsize = 200)
xval= Label(positions, bg ='black', text = '%.3f' %(xpos), font = 'verdana 30', fg = 'white', anchor = 'e', justify = 'right')
xval.grid(row = 1 , column = 1,sticky = 'e')

yval = Label(positions, bg ='black', text = '%.3f' %(ypos), font = 'verdana 30', fg = 'white', anchor = 'e', justify = 'right')
yval.grid(row = 2 , column = 1, sticky = 'e')

zval = Label(positions, bg ='black', text = '%.3f' %(zpos), font = 'verdana 30', fg = 'white', anchor = 'e', justify = 'right')
zval.grid(row = 3 , column = 1,sticky = 'e')

lineval = Label(positions, bg ='black', text = '%3d' %(line), font = 'verdana 30', fg = 'white', anchor = 'e', justify = 'right')
lineval.grid(row = 4 , column = 1,sticky = 'e')

Frame(positions, bg= 'white', width = 2, height = 250).grid(row = 0 ,column =2, rowspan = 5, sticky = 'n' )
#positions.columnconfigure(2, minsize = 5)

#wcss = Frame(midframe, bg = 'black' , borderwidth = 10)
#wcss.pack(side= 'left', fill = 'y')



xwcs = Label(positions, bg ='black', text = 'X:', font = 'verdana 15', fg = 'white')
xwcs.grid(row = 1 , column = 3)
positions.columnconfigure(3, minsize = 60)

ywcs = Label(positions, bg ='black', text = 'Y:', font = 'verdana 15', fg = 'white')
ywcs.grid(row = 2 , column = 3)

xwcs_entry = Entry(positions)
xwcs_entry.grid(row = 1, column = 4)

ywcs_entry = Entry(positions)
ywcs_entry.grid(row = 2, column = 4)

positions.columnconfigure(5, minsize =80)

x_measure = Button(positions, text ='Measure', command = measureX)
x_measure.grid(row = 1, column = 5)

y_measure = Button(positions, text ='Measure', command = measureY)
y_measure.grid(row = 2, column = 5)

enableMeasures()

Frame(positions, bg= 'white', width = 2, height = 250).grid(row = 0 ,column =6, rowspan = 5, sticky = 'n' )
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

enableJOG()

lowerframe = Frame(root,bg='black', height = 300)
lowerframe.pack(fill = 'x')



progframe = Frame(lowerframe, bg = 'black', borderwidth = 10);
progframe.pack(side = 'left', fill = 'y')


scrollbar = Scrollbar(progframe)
prog_show  = Text(progframe , height= 12, width = 75, font = 'verdana 12')
scrollbar.pack(side = 'right', fill = 'y')
prog_show.pack(side = 'top')
scrollbar.config(command=prog_show.yview)
prog_show.config(yscrollcommand=scrollbar.set)

Frame(lowerframe, bg= 'white', width = 2, height = 220, pady = 10).pack(side = 'left')

optionsframe = Frame(lowerframe, bg = 'black', borderwidth = 10)
optionsframe.pack(side = 'left')

strt = Button(optionsframe, text = 'Start', command= start, width = 20)
strt.pack(side = 'top')
Label(optionsframe, bg = 'black', height = 1).pack()
stp = Button(optionsframe, text = 'Stop', command = stop, width = 20)
stp.pack()
Label(optionsframe, bg = 'black', height = 1).pack()

send = Button(optionsframe, text = 'Send File', command= sendFile, width = 20)
send.pack()
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
