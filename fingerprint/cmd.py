import serial
import time
import tkinter


def quit():
    global tkTop
    ser.write(bytes('L', 'UTF-8'))
    tkTop.destroy()

def set_button1_state():
        varLabel.set("ENROLLING")
        for i in range(3):
            print(ser.readline().decode('UTF-8'))
            time.sleep(3)

        # while True:
        #     a = ser.readline().decode('UTF-8')
        #     print(a)
        #     if a != "r":
        #         print("not ready")
        #     time.sleep(3)
        print("enrolling")
        print(ser.readline().decode('UTF-8'))
        time.sleep(1)
        ser.write(bytes('enroll', 'UTF-8'))    
        for i in range(3):
            print(ser.readline().decode('UTF-8'))
            time.sleep(2)
        ser.write(bytes('1', 'UTF-8')) 
        time.sleep(2)
        print(ser.readline().decode('UTF-8'))
        time.sleep(1)
        print(ser.readline().decode('UTF-8'))
        for i in range(5):
            a = ser.readline().decode('UTF-8').strip()
            print(a)
            print(a == ".")
            time.sleep(1)            
        #ser.write(bytes('1', 'UTF-8'))

def set_button2_state():
        varLabel.set("SCANNING")
        ser.write(bytes('S', 'UTF-8'))

ser = serial.Serial('/dev/ttyACM0', 9600)
print("Reset Arduino")
time.sleep(3)
ser.write(bytes('E', 'UTF-8'))

tkTop = tkinter.Tk()
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

tkinter.mainloop()
