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
from auth_util import login_required, check_access_token

conn = pymysql.connect(
        host=DB['host'], 
        port=DB['port'], 
        user=DB['user_id'], 
        password=DB['user_pw'], 
        database=DB['database'], 
        charset=DB['charset'])

cursor = conn.cursor(pymysql.cursors.DictCursor)

Auth_api = Namespace(
    name="Auth",
    description="사용자 인증을 위한 API",
)

user_fields = Auth_api.model('User', {  # Model 객체 생성
    'name': fields.String(required=True)
})

user_fields_auth = Auth_api.inherit('User Auth', user_fields, {
    'pwd': fields.String(drequired=True)
})

user_fields_register = Auth_api.inherit('User Register', user_fields_auth, {
    'tel': fields.String(required=True),
    'email': fields.String(required=True)
})

email_fields = Auth_api.model('Email', {
    'email': fields.String(required=True)
})

jwt_fields = Auth_api.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})

company_fields = Auth_api.model('Company', {
    'company_name': fields.String(required=True),
    'zip_code': fields.String(required=True),
    'address': fields.String(required=True),
    'address_detail': fields.String(required=True),
    'ceo_name': fields.String(required=True),
    'ceo_tel': fields.String(required=True),
    'homepage': fields.String(required=True),
    'created_date': fields.String(required=True),
    'listed': fields.String(required=True),
    'company_vision': fields.String(required=True),
    'company_img': fields.String(required=True, description="company image"),
    'rep_img': fields.String(required=True, description="representative image"),
    'logo': fields.String(required=True, description="logo file")
})

@Auth_api.route('/register')
class AuthRegister(Resource):
    @Auth_api.expect(user_fields_register)
    @Auth_api.doc(description="회원 가입")
    def post(self):
        try:
            email = request.json['email']
            name = request.json['name']
            pwd = request.json['pwd']
            tel = request.json['tel']

            db_conn = conn
            with db_conn.cursor(pymysql.cursors.DictCursor) as cursor:

                if cursor.execute("SELECT * FROM user WHERE email=%s", (email)):
                    return {
                        "message": "User Already Exists"
                    }, 200
                else:
                    pwd_hash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())  # 비밀번호 해싱
                    cursor.execute("INSERT INTO user (email, name, pwd, tel, join_date) VALUES (%s, %s, %s, %s, now())", (email, name, pwd_hash, tel))
                    conn.commit()

                    return {
                        # 'Authorization': jwt.encode({'name': name}, "secret", algorithm="HS256")  # str으로 반환하여 return
                        "message": "Success"
                    }, 200
        except Exception as e:
            db_conn.close()
            return str(e)

@Auth_api.route('/login')
class AuthLogin(Resource):
    @Auth_api.expect(user_fields_auth)
    @Auth_api.doc(description="로그인")
    def post(self):
        try:
            email = request.json['email']
            pwd = request.json['pwd']
            db_conn = conn
            with db_conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT pwd FROM user WHERE email=%s", (email))
                pwd_hash = cursor.fetchone()
                
                if not cursor.execute("SELECT * FROM user WHERE email=%s", (email)):
                    return {
                        "message": "User Not Found"
                    }, 404
                
                elif not bcrypt.checkpw(pwd.encode('utf-8'), pwd_hash['pwd'].encode('utf-8')):  # 비밀번호 일치 확인
                    return {
                        "message": "Auth Failed"
                    }, 404
                else:
                    # 최근 로그인 시간 업데이트
                    sql = "UPDATE user SET recent_login = now() where email = %s"
                    cursor.execute(sql, email)
                    conn.commit()

                    return {
                        'Authorization': jwt.encode({'email': email}, "secret", algorithm="HS256") # str으로 반환하여 return
                    }, 200
                
        except Exception as e:
            db_conn.close()
            return str(e)

@Auth_api.route('/email/check')
class AuthEmailCheck(Resource):
    @Auth_api.expect(email_fields)
    @Auth_api.doc(description="이메일 중복 체크")
    def post(self):
        try:
            email = request.json['email']
            db_conn = conn
            with db_conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM user WHERE email=%s", (email))
                user = cursor.fetchone()
                if user:
                    return {
                        "message": "Failed"
                    }, 200
                else:
                    return {
                        "message": "Success"
                    }, 200
        except Exception as e:
            db_conn.close()
            return str(e)
        
UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@Auth_api.route('/leave', methods = ['POST'])
class leave(Resource):
    @Auth_api.expect(user_fields_auth)
    @Auth_api.doc(description="회원 탈퇴")
    @login_required
    def post(self):
        try:
            name = request.json['name']
            pwd = request.json['pwd']
            db_conn = conn
            with db_conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT pwd FROM user WHERE name=%s", (name))
                pwd_hash = cursor.fetchone()
                if bcrypt.checkpw(pwd.encode('utf-8'), pwd_hash['pwd'].encode('utf-8')):
                    sql = "UPDATE user SET leave_date = now() where name = %s"
                    cursor.execute(sql, name)
                    conn.commit()
            return 'leave success'
        
        except Exception as e:
            db_conn.close()
            return str(e)
    
@Auth_api.route('/company', methods = ['POST'])
class company(Resource):
    @Auth_api.expect(company_fields)
    @Auth_api.doc(description="기업 등록")
    @login_required
    def post(self):
        try:
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
            db_conn = conn
            with db_conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, param)
                conn.commit()
            return 'upload success'
        
        except Exception as e:
            db_conn.close()
            return str(e)
    
@Auth_api.route('/email')
class AuthEmail(Resource):
    @Auth_api.doc(description="토큰 to 이메일")
    @login_required
    def get(self):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            payload = check_access_token(access_token)
            if payload is None:
                return Response(status=401)
        return payload["email"]