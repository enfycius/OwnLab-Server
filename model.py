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

        with open('items.json', 'r', encoding='UTF8') as f:
            items = json.load(f)

        for i in range(len(items)):
            survey_list.append(items['q'+str(i+1)])
        
        return {
            'question': survey_list
        }