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


UPLOAD_FOLDER = 'assets/img'

port_file = open("./port.txt", "r")
serial_port = port_file.readline()

try:
    ser = serial.Serial(serial_port, 9600)
except Exception as e:
    print(e)


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
    global ser
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
    sql = "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(250), email VARCHAR(250), first_name VARCHAR(250), fingerprintID INT(8), img_filename VARCHAR(255))"
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
    # count number of person in db then add one for the id of the next person
    personid = len(cursor.fetchall()) + 1
    cursor.close()
    ser.write(bytes(str(personid), 'UTF-8'))  # utils
    # waiting till id is stored
    while True:
        a = ser.readline().decode('UTF-8').strip()  # utils
        print(a)
        if(a == "FINGERPRINT_NOT_MATCH"):  # error fingerprint not matching
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
    all = cursor.fetchall()
    # count number of person in db then add one for the id of the next person
    personid = len(all) + 1
    ser.write(bytes(str(personid), 'UTF-8'))  # utils
    cursor.close()
    # waiting until step 1 is finished
    while True:
        a = ser.readline().decode('UTF-8').strip()  # utils
        print(a)
        if(a == "REMOVE_HAND"):  # step 1 successfull
            return personid
        # time.sleep(1)


def enroll_step_2():
    a = ""
    # waiting till id is stored
    while True:
        a = ser.readline().decode('UTF-8').strip()  # utils
        print(a)
        if(a == "FINGERPRINT_NOT_MATCH"):  # error fingerprint not matching
            print("fingerPrint didn't match data")
            return False
        if(a == "STORED"):  # successfully stored
            return True
        # time.sleep(1)


def scan():
    a = ""
    # time.sleep(1)
    print("scanning")
    ser.write(bytes('scan', 'UTF-8'))
    while True:
        a = ser.readline().decode('UTF-8').strip()
        if("FOUND_ID#" in a):
            splitted = a.split("#")
            return int(splitted[len(splitted) - 1])
        if(a == "FINGERPRINT_NOTFOUND"):
            return -1


class EnrollStep1(Resource):
    def post(self):
        f = enroll_step_1()
        if(f != 0):
            return {'status': True, 'fingerID': f}, 201, {'Access-Control-Allow-Origin': '*'}
        else:
            return {'status': False}, 400, {'Access-Control-Allow-Origin': '*'}


class EnrollStep2(Resource):
    def post(self):
        f = enroll_step_2()
        if(f):
            return {'status': True}, 201, {'Access-Control-Allow-Origin': '*'}
        else:
            return {'status': False}, 400, {'Access-Control-Allow-Origin': '*'}


class Enroller(Resource):
    def post(self):
        parser.add_argument('name', type=str)
        parser.add_argument('firstName', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('filename', type=str)
        parser.add_argument('fingerprintID', type=str)
        # parser.add_argument('cin', type=str)
        # parser.add_argument('sex', type=int)
        # parser.add_argument('age', type=int)
        # parser.add_argument('situation', type=int)
        # parser.add_argument(
        #     'file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        # print("ARGUMENTS DKFJDLSQJFLQDSJFLK")
        # print(args)
        # enroll_step_1()
        # f = enroll_step_2()
        sql = f"INSERT INTO users(name, first_name, email, img_filename, fingerprintID) VALUES ('{args['name']}', '{args['firstName']}', '{args['email']}', '{args['filename']}', {int(args['fingerprintID'])})"
        print("SQL QUERY")
        print(sql)
        cursor = db_connection.cursor()
        cursor.execute(sql)
        db_connection.commit()
        return {
            'data': '',
            'message': '',
            'status': True
        }, 201, {'Access-Control-Allow-Origin': '*'}
        # if(f):
        #     return {
        #         'name': args['name'],
        #         'first_name': args['firstName'],
        #         'adress': args['adress'],
        #         'cin': args['cin'],
        #         'sex': args['sex'],
        #         'age': args['age'],
        #         'situation': args['situation'],
        #         # 'img_filename': "" + str(args['name']) + str(args['cin']) + ".jpeg"
        #     }, 201, {'Access-Control-Allow-Origin': '*'}
        # else:
        #     return {
        #         'message' : 'there was an error'
        #     }, 400, {'Access-Control-Allow-Origin': '*'}


class PhotoUpload(Resource):
    decorators = []

    def post(self):
        # print("DATADATATATAT")
        data = parser.parse_args()
        # print(data)
        if data['file'] == "":
            return {
                'data': '',
                'message': 'No file found',
                'status': 'error'
            }, 201, {'Access-Control-Allow-Origin': '*'}
        photo = data['file']
        print(photo)

        if photo:
            filename = str(uuid.uuid4()) + ".jpeg"
            photo.save(os.path.join(UPLOAD_FOLDER, filename))
            return {
                'data': filename,
                'message': 'photo uploaded',
                'status': 'success'
            }, 201, {'Access-Control-Allow-Origin': '*'}
        return {
            'data': '',
            'message': 'Something went wrong',
            'status': 'error'
        }, 400, {'Access-Control-Allow-Origin': '*'}


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world', 'nom': 'setra'}, 200, {'Access-Control-Allow-Origin': '*'}


class Scan(Resource):
    def post(self):
        fingerID = scan()
        mycursor = db_connection.cursor()
        mycursor.execute(
            f"SELECT * FROM users WHERE fingerprintID={fingerID}")
        result = mycursor.fetchone()
        # id, name, email, first_name, fingerID, img_filename
        print(result)
        return {'fingerID': result[4], 'name': result[1], 'email': result[2], 'firstname': result[3], 'img_filename': result[5]}


api.add_resource(HelloWorld, '/')
api.add_resource(Enroller, '/enroll')
api.add_resource(PhotoUpload, '/upload')
api.add_resource(EnrollStep1, '/enroll1')
api.add_resource(EnrollStep2, '/enroll2')
api.add_resource(Scan, '/scan')


if __name__ == '__main__':

    # try:
    # 		ser = serial.Serial(serial_port, 9600)
    # except Exception as e:
    # 		print(e)
    # 		pass

    initDatabase()
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    getReady()
    # ser.close()
    app.run(debug=False, use_evalex=False, threaded=True)
