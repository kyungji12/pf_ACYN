from django.shortcuts import render #html파일에 원하는 context인자를 보낼 수 있음
from django.shortcuts import redirect #url만 이동하는 것
import json
import numpy as np
from .make_DF import Model as model
from .report import Report as report

# Create your views here.
def home(request):
    return render(request, 'home.html')

def desc(request):
    return render(request, 'desc.html')

def workout(request):
    return render(request, 'workout.html')

def result(request):
    if request.method == 'POST':
        #데이터 받아오기
        result_data = json.loads(request.body.decode('utf-8'))
        # print(result_data)

        #받아온 데이터를 예측 모델 형태에 맞게 변환하기
        model_data = model.make_data(result_data)
        # print(model_data)
        
        #예측모델에 넣기
        predict_data = model.predict(model_data)
        print(predict_data)


        return render(request, 'result.html')




def video_test(request):
    return render(request, 'video_test.html')
def video_test2(request):
    return render(request, 'video_test2.html')
def video_test3(request):
    return render(request, 'video_test3.html')