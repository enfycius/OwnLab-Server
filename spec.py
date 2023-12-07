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
            name = request.form['name'] # 자격증명
            date = request.form['date'] # 취득일
            publish_org = request.form['publish_org'] # 발행기관
            pass_sep = request.form['pass_sep'] # 합격구분

            cursor.execute("INSERT INTO spec (type_of_spec, name, date, publish_org, pass_sep) VALUES (%s, %s, %s, %s, %s)", (tos, name, date, publish_org, pass_sep))
            conn.commit()

        

            return {'result': 'success'}