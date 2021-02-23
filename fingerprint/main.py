from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import werkzeug
from werkzeug.utils import secure_filename
import os
import time

UPLOAD_FOLDER = 'static/img'


app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'

parser = reqparse.RequestParser()
parser.add_argument('file',type=werkzeug.datastructures.FileStorage, location='files')

def enroll():
    global personid
    # personid += 1
    # varLabel.set("ENROLLING")
    a = ""
    time.sleep(1)
    # ser.write(bytes('enroll', 'UTF-8')) # utils
    print("enrolling")
    # waiting for IDCODE printed by serial
    while a != "IDCODE":
        # a = ser.readline().decode('UTF-8').strip() # utils
        print(a)
        # varLabel.set(a)
        # time.sleep(1)
    # sending id to serial
    # ser.write(bytes(str(personid), 'UTF-8')) # utils
    # waiting till id is stored
    while a != "Stored":
        # a = ser.readline().decode('UTF-8').strip() # utils
        print(a)
        # time.sleep(1)
    return 1

def scan():
    a = ""
    # time.sleep(1)        
    print("scaning")
    # ser.write(bytes('scan', 'UTF-8'))    
    while a != "FOUND_ID":
        # print("waiting for id")
        # a = ser.readline().decode('UTF-8').strip() # utils
        print(a)
        # varLabel.set(a)
        time.sleep(1)
    return "1"

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
        # thefile = request.files['file']
        # filename = secure_filename(thefile.filename)
        # print("saving 1")
        # thefile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print("saved 1")
        # image_file = args['file']
        # filename = secure_filename(image_file.filename)
        # print("saving the file")
        # image_file.save(args[name] + ".jpg")
        return {
            'name': args['name'],
            'first_name': args['firstName'],
            'adress': args['adress'],
            'cin': args['cin'],
            'sex': args['sex'],
            'age': args['age'],
            'situation': args['situation'],
            # 'file': args['file']
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
            filename = 'your_image.jpeg'
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
    app.run(debug=True)