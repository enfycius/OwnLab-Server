import pymysql
import os
from flask import request
from flask_restx import Api, Namespace, Resource, fields
from config import DB
from werkzeug.utils import secure_filename
from auth_util import login_required, check_access_token
from mysql.connector import pooling

conn = pymysql.connect(
        host=DB['host'],
        port=DB['port'],
        user=DB['user_id'],
        password=DB['user_pw'],
        database=DB['database'],
        charset=DB['charset'],
        cursorclass=pymysql.cursors.DictCursor)

connection_pool = pooling.MySQLConnectionPool(
    pool_name = "capstone_pool",
    pool_size = 10,
    pool_reset_session = True,
    host = DB['host'],
    port = DB['port'],
    user = DB['user_id'],
    password = DB['user_pw'],
    database = DB['database'],
    charset = DB['charset']
)

Resume_api = Namespace(
    name="Resume",
    description="이력서 관련 API",
)

resume_fields = Resume_api.model('Resume', {  # Model 객체 생성
    'profile': fields.String(required=True),
    'name': fields.String(required=True),
    'tel': fields.String(required=True),
    'email': fields.String(required=True),
    'birth': fields.String(required=True),
    'sex': fields.String(required=True),
    'address': fields.String(required=True),
    'school': fields.String(required=True),
    'school_state': fields.String(required=True),
    'company_career': fields.String(required=True),
    'part_career': fields.String(required=True),
    'work_time': fields.String(required=True),
    'work_start': fields.String(required=True),
    'work_end': fields.String(required=True),
    'working': fields.Boolean(required=True),
    'work': fields.String(required=True),
    'sido': fields.String(required=True),
    'sigungu': fields.String(required=True),
    'first_work': fields.String(required=True),
    'second_work': fields.String(required=True),
    'work_type': fields.String(required=True),
    'wish_work_term': fields.String(required=True),
    'wish_work_term_etc': fields.String(required=True),
    'wish_salary_type': fields.String(required=True),
    'ps': fields.String(required=True),
    'open_permission': fields.Boolean(required=True)
})

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@Resume_api.route("/add_resume", methods = ['POST'])
class apply_post(Resource):
    @Resume_api.doc(description="공고 지원")
    @login_required
    def post(self):
        try:
            access_token = request.headers.get('Authorization')
            payload = check_access_token(access_token)
            if payload is None:
                return "fail"
            else:
                email = payload['email']

            name = request.form['name']
            tel = request.form['tel']
            birth = request.form['birth']
            sex = request.form['sex']
            address = request.form['address']
            resume_title = request.form['resume_title']
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

            connection_obj = connection_pool.get_connection()
            if connection_obj.is_connected():
                with connection_obj.cursor(pymysql.cursors.DictCursor) as cursor:

                    param = (name, tel, email, birth, sex, address, resume_title, school, school_state, company_career, part_career, work_time, work_start, work_end, working, work, sido, sigungu, first_work, second_work, work_type, wish_work_term, wish_work_term_etc, wish_salary_type, ps, open_permission)

                    columns = [
                        "name", "tel", "email", "birth", "sex", "address",
                        "resume_title", "school", "school_state", "company_career",
                        "part_career", "work_time", "work_start", "work_end", "working",
                        "work", "sido", "sigungu", "first_work", "second_work", "work_type",
                        "wish_work_term", "wish_work_term_etc", "wish_salary_type", "ps", "open_permission"
                    ]

                    values_placeholders = ", ".join(["%s"] * len(columns))
                    columns_string = ", ".join(columns)

                    sql = f"INSERT resume ({columns_string}) VALUES ({values_placeholders})"

                    cursor.execute(sql, param)
                    connection_obj.commit()
                    connection_obj.close()

                    return {
                        "message" : "success"
                    },200
               
        except Exception as e:
            return str(e)