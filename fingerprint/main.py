from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import werkzeug
from werkzeug.utils import secure_filename
import os
import time
import serial
from tinydb import TinyDB, Query
db = TinyDB('user.json')

User = Query()

UPLOAD_FOLDER = 'static/img'

ser = serial.Serial('/dev/ttyACM0', 9600)

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'

parser = reqparse.RequestParser()
parser.add_argument('file',type=werkzeug.datastructures.FileStorage, location='files')

def enroll():
    a = ""
    time.sleep(1)
    ser.write(bytes('enroll', 'UTF-8')) # utils
    print("enrolling")
    # waiting for IDCODE printed by serial
    while a != "IDCODE":
        a = ser.readline().decode('UTF-8').strip() # utils
        print(a)
    # sending id to serial
    personid = len(db) + 1 # getting number of person registered in db then add one for the next person
    ser.write(bytes(str(personid), 'UTF-8')) # utils
    # waiting till id is stored
    while True:
        a = ser.readline().decode('UTF-8').strip() # utils
        print(a)
        if(a == "FINGERPRINT_NOT_MATCH"): # errot fingerprint not matching
            return False
        if(a == "STORED"): # successfully stored
            return True
        # time.sleep(1)
    return True

def enroll_step_1():
    a = ""
    time.sleep(1)
    ser.write(bytes('enroll', 'UTF-8')) # utils
    print("enrolling")
    # waiting for IDCODE printed by serial
    while a != "IDCODE":
        a = ser.readline().decode('UTF-8').strip() # utils
        print(a)
    # sending id to serial
    personid = len(db) + 1 # getting number of person registered in db then add one for the next person
    ser.write(bytes(str(personid), 'UTF-8')) # utils
    # waiting till id is stored
    while True:
        a = ser.readline().decode('UTF-8').strip() # utils
        print(a)
        if(a == "REMOVE_HAND"): # step 1 successfull
            return True
        # time.sleep(1)
    return True

def enroll_step_2():
    a = ""
    # waiting till id is stored
    while True:
        a = ser.readline().decode('UTF-8').strip() # utils
        print(a)
        if(a == "FINGERPRINT_NOT_MATCH"): # errot fingerprint not matching
            return False
        if(a == "STORED"): # successfully stored
            return True
        # time.sleep(1)
    return True

def scan():
    a = ""
    # time.sleep(1)        
    print("scaning")
    # ser.write(bytes('scan', 'UTF-8'))
    toreturn = -1;
    while True:
        try:
            a = ser.readline().decode('UTF-8').strip()
            toreturn = int(a) # try to convert the message to int (if arduino send the ID of the person)
            return toreturn
        except ValueError: # if the message is not convertible to int, then we are on processing phase
            if(a == "FINGERPRINT_NOTFOUND"): # the finger does not match in any of the finger in memory
                return -1

class Enroller(Resource):
    def post(self):
        parser.add_argument('name', type=str)
        parser.add_argument('firstName', type=str)
        parser.add_argument('adress', type=str)
        parser.add_argument('cin', type=str)
        parser.add_argument('sex', type=int)
        parser.add_argument('age', type=int)
        parser.add_argument('situation', type=int)
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        return {
            'name': args['name'],
            'first_name': args['firstName'],
            'adress': args['adress'],
            'cin': args['cin'],
            'sex': args['sex'],
            'age': args['age'],
            'situation': args['situation'],
            'img_filename': "" + str(args['name']) + str(args['cin']) + ".jpeg"
        }, 201, {'Access-Control-Allow-Origin': '*'} 

class PhotoUpload(Resource):
    decorators=[]

    def post(self):
        data = parser.parse_args()
        if data['file'] == "":
            return {
                    'data':'',
                    'message':'No file found',
                    'status':'error'
                    }, 201, {'Access-Control-Allow-Origin': '*'} 
        photo = data['file']

        if photo:
            filename = data['img_filename']
            photo.save(os.path.join(UPLOAD_FOLDER,filename))
            return {
                    'data':'',
                    'message':'photo uploaded',
                    'status':'success'
                    }, 201, {'Access-Control-Allow-Origin': '*'} 
        return {
                'data':'',
                'message':'Something when wrong',
                'status':'error'
                }, 201, {'Access-Control-Allow-Origin': '*'} 



class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world', 'nom': 'setra'}, 201, {'Access-Control-Allow-Origin': '*'} 

api.add_resource(HelloWorld, '/')
api.add_resource(Enroller, '/enroll')
api.add_resource(PhotoUpload,'/upload')

if __name__ == '__main__':
    ms = ""
    # waiting until the arduino is ready
    while ms != "READY":
        ms = ser.readline().decode('UTF-8').strip() # utils
    app.run(debug=True)