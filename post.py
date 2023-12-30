import pymysql
import os
from flask import request
from flask_restx import Api, Namespace, Resource, fields
from config import DB
from werkzeug.utils import secure_filename
from auth_util import login_required, check_access_token

conn = pymysql.connect(
        host=DB['host'], 
        port=DB['port'], 
        user=DB['user_id'], 
        password=DB['user_pw'], 
        database=DB['database'], 
        charset=DB['charset'])

Post_api = Namespace(
    name="Post",
    description="게시글 관련 API",
)

post_fields = Post_api.model('Post', {  # Model 객체 생성
    'title': fields.String(required=True),
    'content': fields.String(required=True),
    'email': fields.String(required=True)
})

@Post_api.route('/add_post', methods = ['POST'])
class add_post(Resource):
    @Post_api.doc(description='게시글 추가')
    @Post_api.expect(post_fields)
    @login_required
    def post(self):
        try:
            access_token = request.headers.get('Authorization')
            payload = check_access_token(access_token)
            if payload is None:
                return "fail"
            else:
                email = payload['email']

            title = request.json['title']
            # content = request.json['content']
            contacts = request.json['contacts']
            assignee = request.json['assignee']
            registration_method = request.json['registration_method']
            address = request.json['address']
            detailed_link = request.json['detailed_link']
            start_date = request.json['start_date']
            end_date = request.json['end_date']

            db_conn = conn
            with db_conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(f"INSERT INTO post (title, contacts, email, assignee, registration_method, address, detailed_link, start_date, end_date, registration_date) VALUES ('{title}', '{contacts}', '{email}', '{assignee}', '{registration_method}', '{address}', '{detailed_link}','{start_date}', '{end_date}', DATE_FORMAT(now() + interval 9 hour, '%Y-%m-%d %H:%i'))")

            db_conn.commit()
            return "success"
        except Exception as e:
            db_conn.close()
            return str(e)
        
@Post_api.route('/get_post', methods = ['GET'])
class get_post(Resource):
    @Post_api.doc(description='게시글 조회')
    @login_required
    def get(self):
        try:
            db_conn = conn
            with db_conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM post")
                posts = cursor.fetchall()
            return posts
        # {"post_items" : posts}
        except Exception as e:
            db_conn.close()
            return str(e)

@Post_api.route('/get_post/<int:post_id>', methods = ['GET'])
class get_post(Resource):
    @Post_api.doc(description='게시글 확인')
    @login_required
    def get(self, post_id):
        try:
            db_conn = conn
            with db_conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(f"SELECT * FROM post WHERE post_id = {post_id}")
                posts = cursor.fetchone()
            return posts
        except Exception as e:
            db_conn.close()
            return str(e)

@Post_api.route('/delete_post/<int:post_id>', methods = ['DELETE'])
class delete_post(Resource):
    @Post_api.doc(description='게시글 삭제')
    @login_required
    def delete(self, post_id):
        try:
            db_conn = conn
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:

                cursor.execute(f"SELECT * FROM post WHERE post_id = {post_id}")
                exist = cursor.fetchone()

                if exist is None:
                    return "fail"
                else:
                    cursor.execute(f"DELETE FROM post WHERE post_id = {post_id}")
                    conn.commit()
                    return "success"
        except Exception as e:
            db_conn.close()
            return str(e)

@Post_api.route('/update_post/<int:post_id>', methods = ['PUT'])
class update_post(Resource):
    @Post_api.doc(description='게시글 수정')
    @login_required
    def put(self, post_id):
        try:
            title = request.json['title']
            content = request.json['content']
            db_conn = conn
            with db_conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(f"UPDATE post SET title = '{title}', content = '{content}' WHERE post_id = {post_id}")
                conn.commit()
                return "success"
            
        except Exception as e:
            conn.close()
            return str(e)