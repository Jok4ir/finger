import serial
import time
import tkinter



def quit():
    global tkTop
    ser.write(bytes('L', 'UTF-8'))
    tkTop.destroy()

def set_button1_state():
    global personid
    personid += 1
    varLabel.set("ENROLLING")
    a = ""
    time.sleep(1)
    ser.write(bytes('enroll', 'UTF-8'))
    print("enrolling")
    # waiting for IDCODE printed by serial
    while a != "IDCODE":
        a = ser.readline().decode('UTF-8').strip()
        print(a)
        varLabel.set(a)
        time.sleep(1)
    # sending id to serial
    ser.write(bytes(str(personid), 'UTF-8'))
    # waiting till id is stored
    while a != "Stored":
        a = ser.readline().decode('UTF-8').strip()
        print(a)
        time.sleep(1)
    # personid += 1

def set_button2_state():
    varLabel.set("SCANNING")
    a = ""
    time.sleep(1)        
    print("scaning")
    ser.write(bytes('scan', 'UTF-8'))    
    while a != "FOUND_ID":
        # print("waiting for id")
        a = ser.readline().decode('UTF-8').strip()
        print(a)
        varLabel.set(a)
        time.sleep(1)

ser = serial.Serial('/dev/ttyACM0', 9600)
print("Reset Arduino")
time.sleep(3)
ser.write(bytes('E', 'UTF-8'))

tkTop = tkinter.Tk()
personid = 1
tkTop.geometry('800x600')
tkTop.title("IoT24hours")
label3 = tkinter.Label(text = 'Building Python GUI to interface an arduino,'
                      '\n and control an LED',font=("Courier", 12,'bold')).pack()
tkTop.counter = 0
b = tkTop.counter

varLabel = tkinter.IntVar()
tkLabel = tkinter.Label(textvariable=varLabel, )
tkLabel.pack()

varLabel2 = tkinter.IntVar()
tkLabel2 = tkinter.Label(textvariable=varLabel2, )
tkLabel2.pack()

button1 = tkinter.IntVar()
button1state = tkinter.Button(tkTop,
    text="ENROLL",
    command=set_button1_state,
    height = 4,
    fg = "black",
    width = 8,
    bd = 5,
    activebackground='green'
)
button1state.pack(side='top', ipadx=10, padx=10, pady=15)

button2 = tkinter.IntVar()
button2state = tkinter.Button(tkTop,
    text="SCAN",
    command=set_button2_state,
    height = 4,
    fg = "black",
    width = 8,
    bd = 5
)
button2state.pack(side='top', ipadx=10, padx=10, pady=15)

tkButtonQuit = tkinter.Button(
    tkTop,
    text="Quit",
    command=quit,
    height = 4,
    fg = "black",
    width = 8,
    bg = 'yellow',
    bd = 5
)
tkButtonQuit.pack(side='top', ipadx=10, padx=10, pady=15)

if __name__ == '__main__':
    a = ""
    while a != "READY":
            a = ser.readline().decode('UTF-8').strip()
            print(a)
            time.sleep(1)
    tkinter.mainloop()

