import serial
import time

def enroll(personid):
    #  personid += 1
    # varLabel.set("ENROLLING")
    a = ""
    time.sleep(1)
    ser.write(bytes('enroll', 'UTF-8'))
    print("enrolling")
    # waiting for IDCODE printed by serial
    while a != "IDCODE":
        a = ser.readline().decode('UTF-8').strip()
        print(a)
        # varLabel.set(a)
        # time.sleep(1)
    # sending id to serial
    ser.write(bytes(str(personid), 'UTF-8'))
    # waiting till id is stored
    while a != "Stored":
        a = ser.readline().decode('UTF-8').strip()
        print(a)
        # time.sleep(1)
    # personid += 1

def enrollstep1(personid):
    #  personid += 1
    # varLabel.set("ENROLLING")
    a = ""
    time.sleep(1)
    ser.write(bytes('enroll', 'UTF-8'))
    print("enrolling")
    # waiting for IDCODE printed by serial
    while a != "IDCODE":
        a = ser.readline().decode('UTF-8').strip()
        print(a)
        # varLabel.set(a)
        time.sleep(1)
    # sending id to serial
    ser.write(bytes(str(personid), 'UTF-8'))
    # waiting till id is stored
    while a != "REMOVE_HAND":
        a = ser.readline().decode('UTF-8').strip()
        print(a)
        time.sleep(1)

def enrollstep2():
    #  personid += 1
    # varLabel.set("ENROLLING")
    a = ""
    time.sleep(1)
    # waiting till id is stored
    while a != "Stored":
        a = ser.readline().decode('UTF-8').strip()
        print(a)
        time.sleep(1)

def scan():
    # varLabel.set("SCANNING")
    a = ""
    time.sleep(1)        
    print("scaning")
    ser.write(bytes('scan', 'UTF-8'))    
    while a != "FOUND_ID":
        # print("waiting for id")
        a = ser.readline().decode('UTF-8').strip()
        print(a)
        # varLabel.set(a)
        time.sleep(1)
    a = ser.readline().decode('UTF-8').strip()
    id = int(a)
    print(id)
    return id


ser = serial.Serial('COM6', 9600)

def init():
    a = ""
    print("Reset Arduino")
    time.sleep(3)
    ser.write(bytes('E', 'UTF-8'))
    while a != "READY":
            a = ser.readline().decode('UTF-8').strip()
            print(a)
            time.sleep(1)