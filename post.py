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
            limitation = request.json['limitation']

            connection_obj = connection_pool.get_connection()
            if connection_obj.is_connected():
                with connection_obj.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = f"INSERT INTO post (title, contacts, email, assignee, registration_method, address, detailed_link, start_date, end_date, registration_date, limitation) VALUES ('{title}', '{contacts}', '{email}', '{assignee}', '{registration_method}', '{address}', '{detailed_link}','{start_date}', '{end_date}', DATE_FORMAT(now() + interval 9 hour, '%Y-%m-%d %H:%i'), {limitation})"
                    cursor.execute(sql)
                    connection_obj.commit()
                    connection_obj.close()
            return {
                "message" : "success"
            },200
        
        except Exception as e:
            return str(e)
        
@Post_api.route("/apply_post", methods = ['POST'])
class apply_post(Resource):
    @Post_api.doc(description="공고 지원")
    @login_required
    def post(self):
        try:
            access_token = request.headers.get('Authorization')
            payload = check_access_token(access_token)
            if payload is None:
                return "fail"
            else:
                email = payload['email']

            post_id = request.json['post_id']
            assignee = request.json['assignee']

            connection_obj = connection_pool.get_connection()
            if connection_obj.is_connected():
                with connection_obj.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = f"SELECT * FROM apply WHERE post_id = {post_id} AND applicant = '{email}'"
                    cursor.execute(sql)
                    result = cursor.fetchall()

                    if result == []:
                        print("It is Blank")
                        print(post_id, assignee, email)
                        sql = f"INSERT INTO apply (post_id, assignee, applicant, registration_date) VALUES ('{post_id}', '{assignee}', '{email}', DATE_FORMAT(now() + interval 9 hour, '%Y-%m-%d %H:%i'))"
                        cursor.execute(sql)

                        sql = f"SELECT * FROM post WHERE post_id = {post_id}"
                        cursor.execute(sql)
                        posts = cursor.fetchall()

                        # 마지막에서 두 번째 Column에서 count 값 Retrieve
                        cursor.execute(f"UPDATE post SET count = {posts[0][-2] + 1} WHERE post_id = {post_id}")
                        connection_obj.commit()
                        connection_obj.close()

                        return {
                            "message" : "success"
                        },200
                    else:
                        print("It is not None:", result)

                        if len(result) != 0:
                            print("Already applied")
                            return {
                                "message" : "Already applied"
                            },200
                        
        except Exception as e:
            return str(e)
        
@Post_api.route('/get_post', methods = ['GET'])
class get_post(Resource):
    @Post_api.doc(description='게시글 조회')
    @login_required
    def get(self):
        try:
            connection_obj = connection_pool.get_connection()
            if connection_obj.is_connected():
                with connection_obj.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = "SELECT * FROM post"
                    cursor.execute(sql)
                    posts = cursor.fetchall()
                    connection_obj.close()

                    keys = ["title", "email", "post_id", "contacts", "assignee", "registration_method", "registration_date", "detailed_link", "address", "start_date", "end_date"]
                    posts = [dict(zip(keys, row)) for row in posts]
                    
                return {"post_items" : posts}
        except Exception as e:
            return str(e)
        finally:
            pass

@Post_api.route('/get_post/<int:post_id>', methods = ['GET'])
class get_post(Resource):
    @Post_api.doc(description='게시글 확인')
    @login_required
    def get(self, post_id):
        try:
            connection_obj = connection_pool.get_connection()
            if connection_obj.is_connected():
                with connection_obj.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = f"SELECT * FROM post WHERE post_id = {post_id}"
                    cursor.execute(sql)
                    posts = cursor.fetchone()
                    connection_obj.close()
            return posts
        except Exception as e:
            return str(e)
        finally:
            pass

@Post_api.route('/delete_post/<int:post_id>', methods = ['DELETE'])
class delete_post(Resource):
    @Post_api.doc(description='게시글 삭제')
    @login_required
    def delete(self, post_id):
        try:
            connection_obj = connection_pool.get_connection()
            if connection_obj.is_connected():
                with connection_obj.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql = f"SELECT * FROM post WHERE post_id = {post_id}"
                    cursor.execute(sql)
                    exist = cursor.fetchone()

                if exist is None:
                    connection_obj.close()
                    return {
                        "message" : "fail"
                    },200
                else:
                    cursor.execute(f"DELETE FROM post WHERE post_id = {post_id}")
                    connection_obj.commit()
                    connection_obj.close()
                    return {
                        "message" : "success"
                    },200
        except Exception as e:
            return str(e)
        finally:
            pass

@Post_api.route('/update_post/<int:post_id>', methods = ['PUT'])
class update_post(Resource):
    @Post_api.doc(description='게시글 수정')
    @login_required
    def put(self, post_id):
        try:
            title = request.json['title']
            content = request.json['content']
            connection_obj = connection_pool.get_connection()
            if connection_obj.is_connected():
                with connection_obj.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute(f"UPDATE post SET title = '{title}', content = '{content}' WHERE post_id = {post_id}")
                    connection_obj.commit()
                    connection_obj.close()
                return {
                    "message" : "success"
                },200
            
        except Exception as e:
            return str(e)
        finally:
            pass

