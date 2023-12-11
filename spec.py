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

Spec_api = Namespace(
    name="Spec",
    description="스펙 관련 API",
)

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@Spec_api.route('/add_spec', methods = ['GET', 'POST'])
class spec_api(Resource):
    def get(self):
        cursor.execute("SELECT * FROM spec")
        specs = cursor.fetchall()
        return specs
    
    def post(self):
        tos = request.form['type_of_spec']
        if tos == '자격증':
            cert_name = request.form['cert_name'] # 자격증명
            cert_inst = request.form['cert_inst'] # 발행기관
            cert_day = request.form['cert_day'] # 취득일
            

            conn.commit()

            return {'result': 'success'}