from flask_restx import Resource, Api, Namespace, fields
from flask import redirect, render_template, request,Response

Model_api = Namespace(
    name="Model",
    description="AI 모델로 보내는 API",
)

@Model_api.route('/')
class Model(Resource):
    def post(self):
        survey_list = []
        # print(request.json)
        for i in range(len(request.json)):
            survey_list.append(request.json["q"+str(i+1)])
        
        return {
            "question": survey_list
        },200