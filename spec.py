import pymysql
import os
from flask import request
from flask_restx import Api, Namespace, Resource, fields
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

spec_fields = Spec_api.model('Spec', {  # Model 객체 생성
    'cert_name': fields.String(required=True),
    'cert_inst': fields.String(required=True),
    'cert_day': fields.String(required=True),
    'award_name': fields.String(required=True),
    'award_inst': fields.String(required=True),
    'award_day': fields.String(required=True),
    'lang_name': fields.String(required=True),
    'lang_day': fields.String(required=True),
    'lang_class': fields.String(required=True),
    'lang_score': fields.String(required=True),
    'lang_acquire': fields.String(required=True),
    'port_name': fields.String(required=True),
    'port_period': fields.String(required=True),
    'port_person': fields.String(required=True),
    'port_tool': fields.String(required=True),
    'port_intro': fields.String(required=True),
    'port_content': fields.String(required=True),
    'intro_name': fields.String(required=True),
    'intro_content': fields.String(required=True)
})

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@Spec_api.route('/add_spec', methods = ['GET', 'POST'])
class spec_api(Resource):
    @Spec_api.doc(description='스펙 조회')
    @Spec_api.response(200, '조회 성공')
    def get(self):
        cursor.execute("SELECT * FROM spec")
        specs = cursor.fetchall()
        return specs
    
    @Spec_api.doc(description='스펙 추가')
    @Spec_api.expect(spec_fields)
    def post(self):
        tos = request.form['type_of_spec']
        email = request.form['email']
        
        cursor.execute("SELECT * FROM spec WHERE email = %s", (email))
        spec = cursor.fetchone()

        print(spec)

        if tos == '자격증':
            cert_name = request.form['cert_name'] # 자격증명
            cert_inst = request.form['cert_inst'] # 발행기관
            cert_day = request.form['cert_day'] # 취득일


            if spec != None:
                cursor.execute("UPDATE spec SET cert_name = %s, cert_inst = %s, cert_day = %s WHERE email = %s", (cert_name, cert_inst, cert_day, email))
            
            else:
                cursor.execute("INSERT INTO spec (cert_name, cert_inst, cert_day) VALUES (%s, %s, %s)", (cert_name, cert_inst, cert_day))
        
        elif tos == '수상':
            award_name = request.form['award_name']
            award_inst = request.form['award_inst']
            award_day = request.form['award_day']

            if spec != None:
                cursor.execute("UPDATE spec SET award_name = %s, award_inst = %s, award_day = %s WHERE email = %s", (award_name, award_inst, award_day, email))

            else:
                cursor.execute("INSERT INTO spec (award_name, award_inst, award_day) VALUES (%s, %s, %s)", (award_name, award_inst, award_day))

        elif tos == '어학':
            lang_name = request.form['lang_name']
            lang_day = request.form['lang_day']
            lang_class = request.form['lang_class']
            lang_score = request.form['lang_score']
            lang_acquire = request.form['lang_acquire']

            if spec != None:
                cursor.execute("UPDATE spec SET lang_name = %s, lang_day = %s, lang_class = %s, lang_score = %s, lang_acquire = %s WHERE email = %s", (lang_name, lang_day, lang_class, lang_score, lang_acquire, email))
            else:
                cursor.execute("INSERT INTO spec (lang_name, lang_day, lang_class, lang_score, lang_acquire) VALUES (%s, %s, %s, %s, %s)", (lang_name, lang_day, lang_class, lang_score, lang_acquire))
            
        elif tos == '포트폴리오':
            port_name = request.form['port_name']
            port_period = request.form['port_period']
            port_person = request.form['port_person']
            port_tool = request.form['port_tool']
            port_intro = request.form['port_intro']
            port_content = request.form['port_content']

            if spec != None:
                cursor.execute("UPDATE spec SET port_name = %s, port_period = %s, port_person = %s, port_tool = %s, port_intro = %s, port_content = %s WHERE email = %s", (port_name, port_period, port_person, port_tool, port_intro, port_content, email))
            else:
                cursor.execute("INSERT INTO spec (port_name, port_period, port_person, port_tool, port_intro, port_content) VALUES (%s, %s, %s, %s, %s, %s)", (port_name, port_period, port_person, port_tool, port_intro, port_content))

        elif tos == '자기소개서':
            intro_name = request.form['intro_name']
            intro_content = request.form['intro_content']

            if spec != None:
                cursor.execute("UPDATE spec SET intro_name = %s, intro_content = %s WHERE email = %s", (intro_name, intro_content, email))
            else:
                cursor.execute("INSERT INTO spec (intro_name, intro_content) VALUES (%s, %s)", (intro_name, intro_content))

        conn.commit()

        return {'result': 'success'}