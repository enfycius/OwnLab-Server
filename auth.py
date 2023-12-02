import jwt
import bcrypt
from flask import redirect, request, flash, send_from_directory, url_for
from flask_restx import Resource, Api, Namespace, fields
from config import DB
import pymysql
import os
from werkzeug.utils import secure_filename

conn = pymysql.connect(
        host=DB['host'], 
        port=DB['port'], 
        user=DB['user_id'], 
        password=DB['user_pw'], 
        database=DB['database'], 
        charset=DB['charset'])

cursor = conn.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * FROM user")

users = cursor.fetchall()

Auth = Namespace(
    name="Auth",
    description="사용자 인증을 위한 API",
)

user_fields = Auth.model('User', {  # Model 객체 생성
    'name': fields.String(description='a User Name', required=True, example="justkode")
})

user_fields_auth = Auth.inherit('User Auth', user_fields, {
    'password': fields.String(description='Password', required=True, example="password")
})

jwt_fields = Auth.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})

@Auth.route('/register')
class AuthRegister(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={500: 'Register Failed'})
    def post(self):
        email = request.json['email']
        name = request.json['name']
        pwd = request.json['pwd']
        tel = request.json['tel']

        if cursor.execute("SELECT * FROM user WHERE email=%s", (email)):
            return {
                "message": "User Already Exists"
            }, 500
        else:
            pwd_hash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())  # 비밀번호 해싱
            cursor.execute("INSERT INTO user (email, name, pwd, tel) VALUES (%s, %s, %s, %s)", (email, name, pwd_hash, tel))
            conn.commit()
            conn.close()

            return {
                'Authorization': jwt.encode({'name': name}, "secret", algorithm="HS256")  # str으로 반환하여 return
            }, 200

@Auth.route('/login')
class AuthLogin(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={404: 'User Not Found'})
    @Auth.doc(responses={500: 'Auth Failed'})
    def post(self):
        name = request.json['name']
        pwd = request.json['pwd']
        cursor.execute("SELECT pwd FROM user WHERE name=%s", (name))
        pwd_hash = cursor.fetchone()
        
        if not cursor.execute("SELECT * FROM user WHERE name=%s", (name)):
            return {
                "message": "User Not Found"
            }, 404
        
        elif not bcrypt.checkpw(pwd.encode('utf-8'), pwd_hash['pwd'].encode('utf-8')):  # 비밀번호 일치 확인
            return {
                "message": "Auth Failed"
            }, 500
        else:
            return {
                'Authorization': jwt.encode({'name': name}, "secret", algorithm="HS256") # str으로 반환하여 return
            }, 200
        
##################################################################################################################
