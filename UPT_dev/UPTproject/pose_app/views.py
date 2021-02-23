from django.shortcuts import render #html파일에 원하는 context인자를 보낼 수 있음
from django.shortcuts import redirect #url만 이동하는 것
from django.http import HttpResponse
import json
import numpy as np
from .make_DF import Model 
from .report import Report

#인스턴스 생성
model = Model()
report = Report()

# Create your views here.
def home(request):
    return render(request, 'home.html')

def desc(request):
    return render(request, 'desc.html')

def workout(request):
    if request.method == 'POST':
        #데이터 받아오기
        result_data = json.loads(request.body.decode('utf-8'))
        # print("🌷제이슨 파일: ",result_data)
        if result_data :
            #받아온 데이터를 예측 모델 형태에 맞게 변환하기
            model_data = model.make_data(result_data)
            model_data_list = model_data.to_json(orient ='columns')
            # print("💜변환 파일: ", model_data.columns.values)
        
            #예측모델에 넣기
            predict_data = model.predict(model_data)
            # print("🎖예측 파일: ",predict_data)

            context = {
                'msg' : '성공', 
                'model' : model_data_list,
                'result' : predict_data
            }
            if predict_data[0] == 0 :
                print("잘못된 자세입니다.")
            elif predict_data[0] == 1 : 
                print("바른 자세입니다!")
            else: 
                print("잘못 촬영됐습니다!")
            return HttpResponse(json.dumps(context), content_type="application/json")
            # return render(request, 'workout.html', context)

    return render(request, 'workout.html')

def result(request):
    # if request.method == 'POST':
    #     #데이터 받아오기
    #     result_data = json.loads(request.body.decode('utf-8'))
    #     print("🌷제이슨 파일: ",result_data)

    #     if result_data :
    #         #받아온 데이터를 예측 모델 형태에 맞게 변환하기
    #         model_data = model.make_data(result_data)
    #         print("💜변환 파일: ",model_data)
        
    #         #예측모델에 넣기
    #         predict_data = model.predict(model_data)
    #         print("🎖예측 파일: ",predict_data)

    #         if predict_data[0] == 0 :
    #             print("잘못된 자세입니다.")
    #         elif predict_data[0] == 1 : 
    #             print("바른 자세입니다!")
    #         else : 
    #             print("잘못 촬영됐습니다!")
            # context = {
            #     'mgs' : '성공', 
            #     'score' : predict_data
            # }
            
        #     return redirect('result', {'score': predict_data[0]})
        # else :
        #     print("잘못 촬영됐습니다!")
            
    return render(request,'result.html')




def video_test(request):
    return render(request, 'video_test.html')
def video_test2(request):
    return render(request, 'video_test2.html')
def video_test3(request):
    return render(request, 'video_test3.html')