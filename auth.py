import datetime
import jwt
import bcrypt
from flask import redirect, render_template, request,Response
from functools import wraps
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

Auth_api = Namespace(
    name="Auth",
    description="사용자 인증을 위한 API",
)

user_fields = Auth_api.model('User', {  # Model 객체 생성
    'name': fields.String(description='a User Name', required=True, example="justkode")
})

user_fields_auth = Auth_api.inherit('User Auth', user_fields, {
    'password': fields.String(description='Password', required=True, example="password")
})

jwt_fields = Auth_api.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})

@Auth_api.route('/register')
class AuthRegister(Resource):
    @Auth_api.expect(user_fields_auth)
    @Auth_api.doc(responses={200: 'Success'})
    @Auth_api.doc(responses={500: 'Register Failed'})
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
            cursor.execute("INSERT INTO user (email, name, pwd, tel, join_date) VALUES (%s, %s, %s, %s, now())", (email, name, pwd_hash, tel))
            conn.commit()
            conn.close()

            return {
                # 'Authorization': jwt.encode({'name': name}, "secret", algorithm="HS256")  # str으로 반환하여 return
                "message": "Success"
            }, 200

@Auth_api.route('/login')
class AuthLogin(Resource):
    @Auth_api.expect(user_fields_auth)
    @Auth_api.doc(responses={200: 'Success'})
    @Auth_api.doc(responses={404: 'User Not Found'})
    @Auth_api.doc(responses={500: 'Auth Failed'})
    def post(self):
        email = request.json['email']
        pwd = request.json['pwd']
        cursor.execute("SELECT pwd FROM user WHERE email=%s", (email))
        pwd_hash = cursor.fetchone()
        
        if not cursor.execute("SELECT * FROM user WHERE email=%s", (email)):
            return {
                "message": "User Not Found"
            }, 404
        
        elif not bcrypt.checkpw(pwd.encode('utf-8'), pwd_hash['pwd'].encode('utf-8')):  # 비밀번호 일치 확인
            return {
                "message": "Auth Failed"
            }, 500
        else:
            # 최근 로그인 시간 업데이트
            sql = "UPDATE user SET recent_login = now() where email = %s"
            cursor.execute(sql, email)
            conn.commit()

            return {
                'Authorization': jwt.encode({'email': email}, "secret", algorithm="HS256") # str으로 반환하여 return
            }, 200
        
@Auth_api.route('/email')
class AuthEmail(Resource):
    def get(self):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            payload = check_access_token(access_token)
            if payload is None:
                return Response(status=401)
        else:
            return Response(status=401)
        return payload

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            payload = check_access_token(access_token)
            if payload is None:
                return Response(status=401)
        else:
            return Response(status=401)
        return f(*args, **kwargs)
    
    return decorated_function

def check_access_token(access_token):
    try:
        payload = jwt.decode(access_token, "secret", algorithms=["HS256"])
        # if payload['exp'] < datetime.utcnow():
        #     payload = None
    except jwt.InvalidTokenError:
        payload = None
    return payload

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@Auth_api.route('/leave', methods = ['GET','POST'])
class leave(Resource):
    def get(self):
        return "hi"
    
    def post(self):
        name = request.json['name']
        pwd = request.json['pwd']
        cursor.execute("SELECT pwd FROM user WHERE name=%s", (name))
        pwd_hash = cursor.fetchone()
        if bcrypt.checkpw(pwd.encode('utf-8'), pwd_hash['pwd'].encode('utf-8')):
            sql = "UPDATE user SET leave_date = now() where name = %s"
            cursor.execute(sql, name)
            conn.commit()
            conn.close()

        return 'leave success'
    
@Auth_api.route('/company', methods = ['POST'])
class company(Resource):
    def post(self):
        name = request.form['name']
        company_name = request.form['company_name']
        zip_code = request.form['zip_code']
        address = request.form['address']
        address_detail = request.form['address_detail']
        ceo_name = request.form['ceo_name']
        ceo_tel = request.form['ceo_tel']
        homepage = request.form['homepage']
        created_date = request.form['created_date']
        listed = request.form['listed']
        company_vision = request.form['company_vision']
        
        company_img = request.files['company_img']
        rep_img = request.files['rep_img']
        logo = request.files['logo']

        # img 파일 저장
        company_img_name = secure_filename(company_img.filename)
        company_path = os.path.join(UPLOAD_FOLDER, company_img_name)
        company_img.save(company_path)

        rep_img_name = secure_filename(rep_img.filename)
        rep_path = os.path.join(UPLOAD_FOLDER, rep_img_name)
        rep_img.save(rep_path)

        logo_name = secure_filename(logo.filename)
        logo_path = os.path.join(UPLOAD_FOLDER, logo_name)
        logo.save(logo_path)

        param = (company_name, zip_code, address, address_detail, ceo_name, ceo_tel, homepage, created_date, listed, company_vision, company_img, rep_img, logo, name)
        sql = "UPDATE company SET company_name = %s, zip_code = %s, address = %s, address_detail = %s, ceo_name = %s, ceo_tel = %s, homepage = %s, created_date = %s, listed = %s, company_vision = %s, company_img = %s, rep_img = %s, logo = %s where name = %s"

        param = (company_path, name)
        sql = "UPDATE company SET company_img = %s where name = %s"
        cursor.execute(sql, param)
        conn.commit()
        conn.close()

        return 'upload success'
