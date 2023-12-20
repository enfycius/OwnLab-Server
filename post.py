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

Post_api = Namespace(
    name="Post",
    description="게시글 관련 API",
)

@Post_api.route('/add_post', methods = ['POST'])
class add_post(Resource):
    def post(self): 
        title = request.json['title']
        content = request.json['content']
        email = request.json['email']
        
        cursor.execute("SELECT * FROM post where title = %s", title)
        posts = cursor.fetchone()
        # print(posts['title'])

        if posts:
            if posts['title'] == title:
                return "fail"
        else:
            cursor.execute(f"INSERT INTO post (title, content, email) VALUES ('{title}', '{content}', '{email}')")
            conn.commit()
            return "success"
        
@Post_api.route('/get_post', methods = ['GET'])
class get_post(Resource):
    def get(self):
        cursor.execute("SELECT * FROM post")
        posts = cursor.fetchall()
        return posts
    
@Post_api.route('/get_post/<int:post_id>', methods = ['GET'])
class get_post(Resource):
    def get(self, post_id):
        cursor.execute(f"SELECT * FROM post WHERE post_id = {post_id}")
        posts = cursor.fetchall()
        return posts
    
@Post_api.route('/delete_post/<int:post_id>', methods = ['DELETE'])
class delete_post(Resource):
    def delete(self, post_id):
        cursor.execute(f"DELETE FROM post WHERE post_id = {post_id}")
        conn.commit()
        return "success"

@Post_api.route('/update_post/<int:post_id>', methods = ['PUT'])
class update_post(Resource):
    def put(self, post_id):
        title = request.json['title']
        content = request.json['content']
        cursor.execute(f"UPDATE post SET title = '{title}', content = '{content}' WHERE post_id = {post_id}")
        conn.commit()
        return "success"