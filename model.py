from flask_restx import Resource, Api, Namespace, fields
from flask import redirect, render_template, request,Response
from auth_util import login_required
import json

Model_api = Namespace(
    name="Model",
    description="AI 모델로 보내는 API",
)

@Model_api.route('/')
class Model(Resource):
    # @login_required
    def get(self):
        survey_list = []
        num_list = []
        all_list = []

        with open('items.json', 'r', encoding='UTF8') as f:
            items = json.load(f)

        for i in range(len(items)):
            num_list.append(i+1)
            survey_list.append(items['q'+str(i+1)])

            temp_list = {
                "id" : num_list[i],
                "question" : survey_list[i]
            }

            all_list.append(temp_list)

        return { 
            "survey_items" : all_list
        }
    
    def post(self):
        result = []

        req_len = len(request.get_json())

        for i in range(req_len):
            temp_checked = request.json[i]['isChecked']
            temp_id = request.json[i]['id']

            temp_list = {
                "ischecked" : temp_checked,
                "id" : temp_id,
                "check_type" : type(temp_checked)
            }

            result.append(temp_list)

        print(result)

        return {
            "code" : 200,
            "message" : "success"
        }