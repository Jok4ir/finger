from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from serial.serialwin32 import Serial
import werkzeug
from werkzeug.utils import secure_filename
import os
import time
import serial
import uuid

from mysql import connector


UPLOAD_FOLDER = 'static/img'

port_file = open("./port.txt", "r")
serial_port = port_file.readline()

try:
    ser = serial.Serial(serial_port, 9600)
except Exception as e:
    print(e)

# ser = serial.Serial(serial_port, 9600)
# ser = serial.serial_for_url(serial_port)
# ser.open()


# mysql = MySQL()
# jaune -> 2
# bleu => 3
# rouge => + 5V
# noir => - GND


app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'toor'
app.config['MYSQL_DATABASE_DB'] = 'fingerprint'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

db_connection = None

db_connection = connector.connect(host=app.config['MYSQL_DATABASE_HOST'], user=app.config['MYSQL_DATABASE_USER'],
                                  passwd=app.config['MYSQL_DATABASE_PASSWORD'], database=app.config['MYSQL_DATABASE_DB'])

parser = reqparse.RequestParser()
parser.add_argument(
    'file', type=werkzeug.datastructures.FileStorage, location='files')

def getReady():
    ms = ""
    # waiting until the arduino is ready
    while True:
        ms = ser.readline().decode('UTF-8').strip()
        print(ms)
        time.sleep(.100)
        if(ms == 'FSETUP'):
            ser.write(bytes('\n', 'UTF-8'))  # utils
        if(ms == 'READY'):
            return 1
def initDatabase():
    # sql = "CREATE DATABASE IF NOT EXISTS fingerprint"
    cursor = db_connection.cursor()
    # cursor.execute(sql)
    # print("database created")
    sql = "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(250), first_name VARCHAR(250), cin VARCHAR(12), sex INT(8), age INT(8), situation INT(8), img_filename VARCHAR(255))"
    cursor.execute(sql)
    print("table created")
    cursor.close()


def enroll():
    a = ""
    time.sleep(1)
    ser.write(bytes('enroll', 'UTF-8'))  # utils
    print("enrolling")
    # waiting for IDCODE printed by serial
    while a != "IDCODE":
        a = ser.readline().decode('UTF-8').strip()  # utils
        print(a)
    # sending id to serial
    sql = "SELECT * FROM users"
    cursor = db_connection.cursor()
    cursor.execute(sql)
    personid = len(cursor.fetchall()) + 1 # count number of person in db then add one for the id of the next person
    cursor.close()
    ser.write(bytes(str(personid), 'UTF-8'))  # utils
    # waiting till id is stored
    while True:
        a = ser.readline().decode('UTF-8').strip()  # utils
        print(a)
        if(a == "FINGERPRINT_NOT_MATCH"):  # errot fingerprint not matching
            return False
        if(a == "STORED"):  # successfully stored
            return True
        # time.sleep(1)
    return True


def enroll_step_1():
    a = ""
    time.sleep(1)
    ser.write(bytes('enroll', 'UTF-8'))  # utils
    print("enrolling")
    # waiting for IDCODE printed by serial
    while a != "IDCODE":
        a = ser.readline().decode('UTF-8').strip()  # utils
        print(a)
    # sending id to serial
    # getting number of person registered in db then add one for the next person
    sql = "SELECT * FROM users"
    cursor = db_connection.cursor()
    cursor.execute(sql)
    personid = len(cursor.fetchall()) + 1 # count number of person in db then add one for the id of the next person
    cursor.close()
    ser.write(bytes(str(personid), 'UTF-8'))  # utils
    ser.write(bytes(str(personid), 'UTF-8'))  # utils
    # waiting till id is stored
    while True:
        a = ser.readline().decode('UTF-8').strip()  # utils
        print(a)
        if(a == "REMOVE_HAND"):  # step 1 successfull
            return True
        # time.sleep(1)
    return True


def enroll_step_2():
    a = ""
    # waiting till id is stored
    while True:
        a = ser.readline().decode('UTF-8').strip()  # utils
        print(a)
        if(a == "FINGERPRINT_NOT_MATCH"):  # errot fingerprint not matching
            print("fingerPrint didn't match dada")
            return False
        if(a == "STORED"):  # successfully stored
            return True
        # time.sleep(1)
    return True


def scan():
    a = ""
    # time.sleep(1)
    print("scaning")
    # ser.write(bytes('scan', 'UTF-8'))
    toreturn = -1
    while True:
        try:
            a = ser.readline().decode('UTF-8').strip()
            # try to convert the message to int (if arduino send the ID of the person)
            toreturn = int(a)
            return toreturn
        except ValueError:  # if the message is not convertible to int, then we are on processing phase
            if(a == "FINGERPRINT_NOTFOUND"):  # the finger does not match in any of the finger in memory
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
        parser.add_argument(
            'file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        enroll_step_1()
        f = enroll_step_2()
        if(f):
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
        else:
            return {
                'message' : 'there was an error'
            }, 400, {'Access-Control-Allow-Origin': '*'}

        


class PhotoUpload(Resource):
    decorators = []

    def post(self):
        data = parser.parse_args()
        print(data)
        if data['file'] == "":
            return {
                'data': '',
                'message': 'No file found',
                'status': 'error'
            }, 201, {'Access-Control-Allow-Origin': '*'}
        photo = data['file']

        if photo:
            filename = str(uuid.uuid4()) + ".jpeg"
            photo.save(os.path.join(UPLOAD_FOLDER, filename))
            return {
                'data': '',
                'message': 'photo uploaded',
                'status': 'success'
            }, 201, {'Access-Control-Allow-Origin': '*'}
        return {
            'data': '',
            'message': 'Something when wrong',
            'status': 'error'
        }, 201, {'Access-Control-Allow-Origin': '*'}


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world', 'nom': 'setra'}, 200, {'Access-Control-Allow-Origin': '*'}


api.add_resource(HelloWorld, '/')
api.add_resource(Enroller, '/enroll')
api.add_resource(PhotoUpload, '/upload')

if __name__ == '__main__':
    
    # try:
    #     ser = serial.Serial(serial_port, 9600)
    # except Exception as e:
    #     print(e)
    #     pass
        
    initDatabase()
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    getReady()
    #ser.close()
    app.run(debug=False, use_evalex=False, threaded=True)
