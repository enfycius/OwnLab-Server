import jwt
import bcrypt
from flask import redirect, request, flash, send_from_directory, url_for
from flask_restx import Resource, Api, Namespace, fields
from config import DB
import pymysql

conn = pymysql.connect(
        host=DB['host'], 
        port=DB['port'], 
        user=DB['user_id'], 
        password=DB['user_pw'], 
        database=DB['database'], 
        charset=DB['charset'])

cursor = conn.cursor(pymysql.cursors.DictCursor)

Resume = Namespace(
    name="Resume",
    description="이력서 관련 API",
)

@Resume.route('/resume')
class resume_api(Resource):
    def get(self):
        cursor.execute("SELECT * FROM resume")
        resumes = cursor.fetchall()
        return resumes
    
    def post(self):
        name = request.form['name']
        tel = request.form['tel']
        email = request.form['email']
        birth = request.form['birth']
        sex = request.form['sex']
        address = request.form['address']
        school = request.form['school']
        school_state = request.form['school_state']
        company_career = request.form['company_career']
        part_career = request.form['part_career']
        work_time = request.form['work_time']
        work_start = request.form['work_start']
        work_end = request.form['work_end']
        working = request.form['working']
        work = request.form['work']
        sido = request.form['sido']
        sigungu = request.form['sigungu']
        first_work = request.form['first_work']
        second_work = request.form['second_work']
        work_type = request.form['work_type']
        wish_work_term = request.form['wish_work_term']
        wish_work_term_etc = request.form['wish_work_term_etc']
        wish_salary_type = request.form['wish_salary_type']
        ps = request.form['ps']
        open_permission = request.form['open_permission']

        sql = "INSERT resume (name, tel, email, birth, sex, address, school, school_state, company_career, part_career, work_time, work_start, work_end, working, work, sido, sigungu, first_work, second_work, work_type, wish_work_term, wish_work_term_etc, wish_salary_type, ps, open_permission) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)", (name, tel, email, birth, sex, address, school, school_state, company_career, part_career, work_time, work_start, work_end, working, work, sido, sigungu, first_work, second_work, work_type, wish_work_term, wish_work_term_etc, wish_salary_type, ps, open_permission)

        cursor.execute(sql)
        conn.commit()
        conn.close()
        return {
            "message": "Success"
        }, 200
    
from werkzeug.utils import secure_filename
import os

image_path = os.path.join('static', 'images')

@Resume.route('/upload')
class file_upload(Resource):
    def post(self):
        file = request.files['file']
        
        filename = secure_filename(file.filename)
        os.mkdirs(image_path, exists_ok=True)
        file.save(os.path.join(image_path, filename))
        cursor.execute("INSERT INTO resume (profile) VALUES (%s)", (filename))
        file_url = cursor.fetchall()
        return file_url