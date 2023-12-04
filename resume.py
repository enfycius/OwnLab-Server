import pymysql
import os
from flask import request
from flask_restx import Api, Namespace, Resource
from config import DB
from werkzeug.utils import secure_filename

conn = pymysql.connect(
        host=DB['host'], 
        port=DB['port'], 
        user=DB['user_id'], 
        password=DB['user_pw'], 
        database=DB['database'], 
        charset=DB['charset'])

cursor = conn.cursor(pymysql.cursors.DictCursor)

Resume_api = Namespace(
    name="Resume",
    description="이력서 관련 API",
)

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@Resume_api.route('/add_resume', methods = ['GET', 'POST'])
class add_resume(Resource):
    def get(self):
        cursor.execute("SELECT * FROM resume")
        resumes = cursor.fetchall()
        return resumes
    
    def post(self): 
        profile = request.files['file']
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

        filename = secure_filename(profile.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        profile.save(file_path)

        param = (file_path, name, tel, email, birth, sex, address, school, school_state, company_career, part_career, work_time, work_start, work_end, working, work, sido, sigungu, first_work, second_work, work_type, wish_work_term, wish_work_term_etc, wish_salary_type, ps, open_permission)

        sql = "INSERT resume (profile, name, tel, email, birth, sex, address, school, school_state, company_career, part_career, work_time, work_start, work_end, working, work, sido, sigungu, first_work, second_work, work_type, wish_work_term, wish_work_term_etc, wish_salary_type, ps, open_permission) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(sql, param)
        conn.commit()
        conn.close()

        return {
            "message": "Success"
        }, 200
    
