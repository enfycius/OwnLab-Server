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

            cursor.execute("INSERT INTO spec (cert_name, cert_inst, cert_day) VALUES (%s, %s, %s)", (cert_name, cert_inst, cert_day))
        
        elif tos == '수상':
            award_name = request.form['award_name']
            award_inst = request.form['award_inst']
            award_day = request.form['award_day']

            cursor.execute("INSERT INTO spec (award_name, award_inst, award_day) VALUES (%s, %s, %s)", (award_name, award_inst, award_day))

        elif tos == '어학':
            lang_name = request.form['lang_name']
            lang_inst = request.form['lang_inst']
            lang_day = request.form['lang_day']
            lang_score = request.form['lang_score']

            cursor.execute("INSERT INTO spec (lang_name, lang_inst, lang_day, lang_score) VALUES (%s, %s, %s, %s)", (lang_name, lang_inst, lang_day, lang_score))
            
        elif tos == '포트폴리오':
            port_name = request.form['port_name']
            port_period = request.form['port_period']
            port_person = request.form['port_person']
            port_tool = request.form['port_tool']
            port_intro = request.form['port_intro']
            port_content = request.form['port_content']

            cursor.execute("INSERT INTO spec (port_name, port_period, port_person, port_tool, port_intro, port_content) VALUES (%s, %s, %s, %s, %s, %s)", (port_name, port_period, port_person, port_tool, port_intro, port_content))

        elif tos == '자기소개서':
            intro_name = request.form['intro_name']
            intro_content = request.form['intro_content']

            cursor.execute("INSERT INTO spec (intro_name, intro_content) VALUES (%s, %s)", (intro_name, intro_content))

        conn.commit()

        return {'result': 'success'}