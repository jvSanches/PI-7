import time
from tkinter import*
from tkinter import filedialog
import struct

import GCode_parser
import modbus_sender
"""
Implementação da interface e inserção das funções modbus 

"""

connection_state = False

xpos, ypos, zpos, line = 0, 0, 0, 0
x_offset, y_offset = 0, 0
last_line = 1000
running = 0
loaded_prog = []

'''Funções de interface'''
# Habilita botões de JOG
def enableJOG():
    jogzpositive.config(state = 'normal')
    jogznegative.config(state = 'normal')
    jogxpositive.config(state = 'normal')
    jogxnegative.config(state = 'normal')
    jogypositive.config(state = 'normal')
    jogynegative.config(state = 'normal')

# Desabilita botões de JOG
def disableJOG():
    jogzpositive.config(state = 'disabled')
    jogznegative.config(state = 'disabled')
    jogxpositive.config(state = 'disabled')
    jogxnegative.config(state = 'disabled')
    jogypositive.config(state = 'disabled')
    jogynegative.config(state = 'disabled')

# Abre GCode de um arquivo
def openFile():
    global prog_show, loaded_prog
    filename = filedialog.askopenfilename()
    try:
        file = open(filename,'r')
        loaded_prog = []
        for i in file:
            loaded_prog.append(i.rstrip())
        for k in range(len(loaded_prog)):
            loaded_prog[k] = loaded_prog[k]
        file.close()
    except:
        pass
    prog_show.delete('1.0','end-1c')
    for l in loaded_prog:
        prog_show.insert(END, l+"\n" )

# Limpa programa do arquivo de texto
def clear():
    global prog_show
    prog_show.delete('0.0',END)

# Atualiza coordenadas
def updateCoords():
    global root, xpos, ypos, zpos, line
    dateAndTime.config(text = '%s' %(time.ctime()))

    if connection_state:        
        nXpos, nYpos, nZpos, nLine = modbus_sender.receiveXYZ()
        if nXpos != None:
            xpos = nXpos
        if nYpos != None:
            ypos = nYpos
        if nYpos != None:
            zpos = nZpos
        if nLine != None:
            line = nLine
        if running and line >= last_line:
            stop()
        xval.config(text = '%.1f' %(xpos-x_offset))
        yval.config(text = '%.1f' %(ypos-y_offset))
        zval.config(text = '%.1f' %(zpos))
        lineval.config(text = '%d' %(line))

# Atualiza horário
def updateTime():
    root.after(100, updateTime)
    updateCoords()

# Desabilita offsets
def disableMeasures():
    global x_measure, y_measure
    x_measure.config(state = 'disabled')
    y_measure.config(state = 'disabled')

# Habilita offsets
def enableMeasures():
    global x_measure, y_measure
    x_measure.config(state = 'normal')
    y_measure.config(state = 'normal')

# Marca offset de X
def measureX():
    global x_offset
    offset = float(xwcs_entry.get())
    x_offset = xpos - offset

# Marca offset de Y
def measureY():
    global y_offset
    offset = float(ywcs_entry.get())
    y_offset = ypos - offset

'''Funções de comunicação'''
# Conecta na porta
def doConnection():
    global connection_state

    if not connection_state:
        try:
            port = port_entry.get()
            if port == "": port = "COM8"
            modbus_sender.LPC_connect(port)
            port_entry.config(state ='disabled')
            con_status.config(text = 'Machine Connected', fg= 'green')
            connect.config(text = 'Disconnect')
            strt.config(state = 'normal')
            send.config(state = 'normal')
            ref_buttom.config(state = 'normal')
            connection_state = True
        except:
            print("Could not connect")
    else:
        modbus_sender.LPC_disconnect()
        port_entry.config(state = 'normal')
        con_status.config(text = 'Machine not Connected', fg = 'red')
        connect.config(text = 'Connect')
        strt.config(state = 'disabled')
        send.config(state = 'disabled')
        ref_buttom.config(state = 'disabled')
        connection_state = False

# Seta referência na LPC
def REF():
    try:
        modbus_sender.WriteSingleRegister(1,9,1)
    except:
        print("Not Connected")

# Funções de JOG
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

# Envia programa para LPC
def sendFile():
    global loaded_prog, last_line
    loaded_prog = prog_show.get("1.0", "end-1c")
    coords = GCode_parser.parse(loaded_prog)
    last_line = len(coords)
    print(coords)
    coords = [[line[0]+x_offset, line[1]+y_offset, line[2]] for line in coords]
    
    try:
        modbus_sender.WriteSingleRegister(1,10,0)
        time.sleep(1)
        modbus_sender.sendLines(1, coords)
        strt.config(state = 'normal')
        print("Fim de envio")
    except:
        print("Not Connected")

# Começa a execução de programa
def start():
    global running
    try:
        modbus_sender.WriteSingleRegister(1,0,1)
        disableJOG()
        time.sleep(0.15)
        running = 1
        strt.config(state = 'disabled')
        stp.config(state = 'normal')
        paus.config(state = 'normal')
        send.config(state = 'disabled')
        ref_buttom.config(state = 'disabled')
    except:
        print("Not Connected")

# Pára a execução de programa
def stop():
    global running
    try:
        enableJOG()
        modbus_sender.WriteSingleRegister(1,1,1)
        running = 0
        strt.config(state = 'normal')
        stp.config(state = 'disabled')
        paus.config(state = 'disabled')
        cont.config(state = 'disabled')
        send.config(state = 'normal')
        ref_buttom.config(state = 'normal')
    except:
        print("Not Connected")

# Pausa a máquina
def suspend():
    global running
    try:
        modbus_sender.WriteSingleRegister(1,3,1)
        running = 0
        strt.config(state = 'disabled')
        stp.config(state = 'normal')
        paus.config(state = 'disabled')
        cont.config(state = 'normal')
    except:
        print("Not Connected")

# Resume o funcionamento da máquina
def resume():
    global running
    try:
        modbus_sender.WriteSingleRegister(1,2,1)
        disableJOG()
        running = 1
        strt.config(state = 'disabled')
        stp.config(state = 'normal')
        paus.config(state = 'normal')
        cont.config(state = 'disabled')
    except:
        print("Not Connected")

'''Definição da interface'''
### Janela principal
root = Tk()
root.title('PI7 Controller')
root.resizable(width=False, height=False)

### Bloco superior
upperframe = Frame(root, bg = 'black')
upperframe.pack(side= 'top')

# Logo
logo = Label(upperframe, text ='PI-7', fg = 'blue', bg = 'black',\
             font = "Times 50 bold  ", width = 5)
logo.pack(side = 'left')
Frame(upperframe, bg= 'white', width = 5).pack(fill = 'y', side = 'left')

# Relógio
clock = Frame(upperframe, bg = 'black')
clock.pack(side = 'left')
dateAndTime= Label(clock, bg = 'black', fg = 'white' , text = '%s' %(time.ctime()), font = 'verdana 12 bold', width = 40)
dateAndTime.grid(row = 0)

# Bloco de conexão
connection = Frame(upperframe, bg = 'black', borderwidth = 10)
connection.pack(side = 'right')
connection.columnconfigure(0, minsize = 150)
# Entrada de texto
con_port = Label(connection, text = 'Port to Connect:', fg = 'white', bg = 'black')
con_port.grid(row = 0, column =0, sticky = 'e' )
port_entry = Entry(connection)
port_entry.grid(row = 0, column = 1)
# Mensagem de status
con_status = Label(connection, text = 'Machine not Connected', fg = 'red', bg = 'black')
con_status.grid(row =1 , column =0, sticky = 'e' )
# Botão
connect = Button(connection, text = 'Connect', bg= 'light gray', command = doConnection)
connect.grid(row = 1, column = 1)
Frame(upperframe, bg= 'white', width = 5).pack(fill = 'y', side = 'left')

Frame(root, bg= 'white', height = 5).pack(fill = 'x', side = 'top')


# Segunda linha de blocos
midframe = Frame(root,bg = 'black')
midframe.pack(side = 'top', fill = 'x')

# Visualização de coordenadas
positions = Frame(midframe, bg = 'black' , height = 300, borderwidth = 10)
positions.pack(side= 'left')
positions.columnconfigure(0, minsize = 60)
positions.columnconfigure(1, minsize = 200)
positions.columnconfigure(3, minsize = 60)
positions.columnconfigure(5, minsize = 80)
# Título
positiontitle = Label(positions, bg ='black', text = 'Position', font = 'verdana 15', fg = 'white')
positiontitle.grid(row = 0, columnspan = 2)
# X
xlabel = Label(positions, bg ='black', text = 'X:', font = 'verdana 30', fg = 'white')
xlabel.grid(row = 1 , column = 0)
xval= Label(positions, bg ='black', text = '%.1f' %(xpos), font = 'verdana 30', fg = 'white', anchor = 'e', justify = 'right')
xval.grid(row = 1 , column = 1,sticky = 'e')
# Y
ylabel = Label(positions, bg ='black', text = 'Y:', font = 'verdana 30', fg = 'white')
ylabel.grid(row = 2 , column = 0)
yval = Label(positions, bg ='black', text = '%.1f' %(ypos), font = 'verdana 30', fg = 'white', anchor = 'e', justify = 'right')
yval.grid(row = 2 , column = 1, sticky = 'e')
# Z
zlabel = Label(positions, bg ='black', text = 'Z:', font = 'verdana 30', fg = 'white')
zlabel.grid(row = 3 , column = 0)
zval = Label(positions, bg ='black', text = '%.1f' %(zpos), font = 'verdana 30', fg = 'white', anchor = 'e', justify = 'right')
zval.grid(row = 3 , column = 1,sticky = 'e')
# Linha
linelabel = Label(positions, bg ='black', text = 'Line:', font = 'verdana 30', fg = 'white')
linelabel.grid(row = 4 , column = 0)
lineval = Label(positions, bg ='black', text = '%3d' %(line), font = 'verdana 30', fg = 'white', anchor = 'e', justify = 'right')
lineval.grid(row = 4 , column = 1,sticky = 'e')

# Medidas
Frame(positions, bg= 'white', width = 2, height = 250).grid(row = 0 ,column =2, rowspan = 5, sticky = 'n' )
# X
xwcs = Label(positions, bg ='black', text = 'X:', font = 'verdana 15', fg = 'white')
xwcs.grid(row = 1 , column = 3)
xwcs_entry = Entry(positions)
xwcs_entry.grid(row = 1, column = 4)
x_measure = Button(positions, text ='Measure', command = measureX)
x_measure.grid(row = 1, column = 5)
# Y
ywcs = Label(positions, bg ='black', text = 'Y:', font = 'verdana 15', fg = 'white')
ywcs.grid(row = 2 , column = 3)
ywcs_entry = Entry(positions)
ywcs_entry.grid(row = 2, column = 4)
y_measure = Button(positions, text ='Measure', command = measureY)
y_measure.grid(row = 2, column = 5)

enableMeasures()

Frame(positions, bg= 'white', width = 2, height = 250).grid(row = 0 ,column =6, rowspan = 5, sticky = 'n' )

# Jog
Frame(root, bg= 'white', height = 5).pack(fill = 'x', side = 'top')
jogframe = Frame(midframe, bg = 'black', borderwidth = 10)
jogframe.pack(side ='left', fill = 'both')
# Botões
enable_jog = Button(jogframe, text= 'Enable JOG', command = enableJOG)
enable_jog.grid(row = 0, column = 0, sticky = 'N')
disable_jog = Button(jogframe, text= 'Disable JOG', command = disableJOG)
disable_jog.grid(row = 0, column = 4, sticky = 'N')
# Z
jogframe.rowconfigure(1, minsize = 20)
jogzpositive = Button(jogframe, text = 'Z+', font = 'verdana 12 bold ', command = jogzmore)
jogzpositive.grid(row=2,column =0)
jogznegative = Button(jogframe, text = 'Z-', font = 'verdana 12 bold ', command = jogzless)
jogznegative.grid(row=4,column =0)
# X
jogxpositive = Button(jogframe, text = 'X+', font = 'verdana 12 bold ', command = jogxmore)
jogxpositive.grid(row=3,column =3)
jogxnegative = Button(jogframe, text = 'X-', font = 'verdana 12 bold ', command = jogxless)
jogxnegative.grid(row=3,column =1)
# Y
jogypositive = Button(jogframe, text = 'Y+', font = 'verdana 12 bold ', command = jogymore)
jogypositive.grid(row=2,column =2)
jogynegative = Button(jogframe, text = 'Y-', font = 'verdana 12 bold ', command = jogyless)
jogynegative.grid(row=4,column =2)

enableJOG()

### Linha inferior
lowerframe = Frame(root,bg='black', height = 300)
lowerframe.pack(fill = 'x')
Frame(lowerframe, bg= 'white', width = 2, height = 220, pady = 10).pack(side = 'left')

# Caixa de texto para programa
progframe = Frame(lowerframe, bg = 'black', borderwidth = 10)
progframe.pack(side = 'left', fill = 'y')
scrollbar = Scrollbar(progframe)
prog_show  = Text(progframe , height= 12, width = 75, font = 'verdana 12')
scrollbar.pack(side = 'right', fill = 'y')
prog_show.pack(side = 'top')
scrollbar.config(command=prog_show.yview)
prog_show.config(yscrollcommand=scrollbar.set)

# Botões
optionsframe = Frame(lowerframe, bg = 'black', borderwidth = 9)
optionsframe.pack(side = 'left')

strt = Button(optionsframe, text = 'Start', command= start, width = 9)
strt.grid(row = 0, column = 0)
strt.config(state = 'disabled')

stp = Button(optionsframe, text = 'Stop', command = stop, width = 9)
stp.grid(row = 0, column = 1)
stp.config(state = 'disabled')

Label(optionsframe, bg = 'black', height = 1).grid(row = 1, columnspan = 2)

paus = Button(optionsframe, text = 'Pause', command= suspend, width = 9)
paus.grid(row = 2, column = 0)
paus.config(state = 'disabled')

cont = Button(optionsframe, text = 'Resume', command = resume, width = 9)
cont.grid(row = 2, column = 1)
cont.config(state = 'disabled')

Label(optionsframe, bg = 'black', height = 1).grid(row = 3, columnspan = 2)

send = Button(optionsframe, text = 'Send File', command= sendFile, width = 20)
send.grid(row = 4, columnspan = 2)
send.config(state = 'disabled')

Label(optionsframe, bg = 'black', height = 1).grid(row = 5, columnspan = 2)

ref_buttom = Button(optionsframe, text = 'REF machine', command = REF)
ref_buttom.grid(row = 6, columnspan = 2)
ref_buttom.config(state = 'disabled')
Label(optionsframe, bg = 'black', height = 1).grid(row = 7, columnspan = 2)

browse_button = Button(optionsframe, text = 'Open File', command = openFile, width = 9)
browse_button.grid(row = 8, column = 0)

rld_button = Button(optionsframe, text = 'Clear', command = clear, width = 9)
rld_button.grid(row = 8, column = 1)

# Habilita atualizações do tempo
updateTime()
# Loop principal
root.mainloop()
