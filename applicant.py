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
        charset=DB['charset'])

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

Applicant_api = Namespace(
    name="Applicant",
    description="지원자 관련 API",
)

applicant_fields = Applicant_api.model('Applicant', {  # Model 객체 생성
    'profile': fields.String(required=True),
    'name': fields.String(required=True),
    'tel': fields.String(required=True),
})

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@Applicant_api.route('/get_applicant', methods = ['POST'])
class get_post(Resource):
    @Applicant_api.doc(description='지원자 조회')
    @login_required
    def post(self):
        try:
            access_token = request.headers.get('Authorization')
            payload = check_access_token(access_token)

            if payload is None:
                return "fail"
            else:
                email = payload['email']

            connection_obj = connection_pool.get_connection()
            if connection_obj.is_connected():
                with connection_obj.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = f"SELECT * FROM apply WHERE assignee = '{email}'"
                    cursor.execute(sql)
                    posts = cursor.fetchall()

                    keys = ["assignee", "post_id", "registration_date"]
                    posts = [dict(zip(keys, row)) for row in posts]

                    sql = f"SELECT name, tel FROM user WHERE email ='{email}'"
                    cursor.execute(sql)
                    users = cursor.fetchall()
                    print(users[0])

                    for post in posts:
                        post["applicant"] = users[0][0]
                        post["tel"] = users[0][1]
                        post["email"] = f"{email}"

                return {"applicant_info" : posts}

        except Exception as e:
            print(str(e))
            return str(e)
        finally:
            connection_obj.close()