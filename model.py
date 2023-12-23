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
        work_time = request.json['work_time']

        for i in range(req_len):
            checked = request.json["survey_results"][i]['isChecked']
            id = request.json["survey_results"][i]['id']

            if checked == True:
                result.append(id)

        return call_model(result, 1, work_time)[1]['checklist']

import pandas as pd

def call_model(input_data, index_of_data, worktime):
    data = {
        index_of_data : { 'voteCount':0, 'votePoint':0, 'answerCount':0, 'total_work_time':0,
                'checklist' : {'passion_ch' : 0, 'cooperation_ch':0, 'diligence_ch':0, 'responsibility_ch':0, 'conductivity_ch':0, 'leadership_ch':0},
                'text_score' : {'passion_tx' : 0, 'cooperation_tx':0, 'diligence_tx':0, 'responsibility_tx':0, 'conductivity_tx':0, 'leadership_tx':0},
                'total_score' : {'passion' : 0, 'cooperation':0, 'diligence':0, 'responsibility':0, 'conductivity':0, 'leadership':0}
                }
    }

    pas = [1,2,3]
    coop = [4,5,6]
    dil = [7,8,9]
    res = [10,11,12]
    con = [13,14,15]
    lead = [16,17,18]

    works = pd.read_excel("아르바이트 직종 분류.xlsx")
    works = works.loc[:, ['직무', '등급']]
    works = works.dropna(axis=0)
    workname = list(works['직무'])
    workscore = list(works['등급'])
    work_class = dict(zip(workname, workscore))
    work_score = {'A' : 1, 'B' : 0.9, 'C' : 0.8, 'D' : 0.7}

    # data[index_of_data]['total_work_time'] += input_ch['work_time(h)']
    # input_ch = {'userID':index_of_data, 'voteID':'00002', 'work_time(h)':30, 'work_name': '판촉도우미', 'checklist':input_data, 'text':'우리 알바생은 요... 성실해요!'}
    input_ch = {'userID':index_of_data, 'work_time(h)':30, 'work_name': '판촉도우미', 'checklist':input_data, 'text':'우리 알바생은 요... 성실해요!'}


    for p in pas:
        if p in input_ch['checklist']:
            data[index_of_data]['checklist']['passion_ch'] += 1*input_ch['work_time(h)']*work_score[work_class[input_ch['work_name']]]
            data[index_of_data]['votePoint'] += 1
    for p in coop:
        if p in input_ch['checklist']:
            data[index_of_data]['checklist']['cooperation_ch'] += 1*input_ch['work_time(h)']*work_score[work_class[input_ch['work_name']]]
            data[index_of_data]['votePoint'] += 1
    for p in dil:
        if p in input_ch['checklist']:
            data[index_of_data]['checklist']['diligence_ch'] += 1*input_ch['work_time(h)']*work_score[work_class[input_ch['work_name']]]
            data[index_of_data]['votePoint'] += 1
    for p in res:
        if p in input_ch['checklist']:
            data[index_of_data]['checklist']['responsibility_ch'] += 1*input_ch['work_time(h)']*work_score[work_class[input_ch['work_name']]]
            data[index_of_data]['votePoint'] += 1
    for p in con:
        if p in input_ch['checklist']:
            data[index_of_data]['checklist']['conductivity_ch'] += 1*input_ch['work_time(h)']*work_score[work_class[input_ch['work_name']]]
            data[index_of_data]['votePoint'] += 1
    for p in lead:
        if p in input_ch['checklist']:
            data[index_of_data]['checklist']['leadership_ch'] += 1*input_ch['work_time(h)']*work_score[work_class[input_ch['work_name']]]
            data[index_of_data]['votePoint'] += 1
            
    data[index_of_data]['voteCount'] += 1

    return data