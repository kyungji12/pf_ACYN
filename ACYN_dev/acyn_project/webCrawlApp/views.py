from django.shortcuts import render #html파일에 원하는 context인자를 보낼 수 있음
from django.shortcuts import redirect #url만 이동하는 것

# from django.http import HttpResponse
from .models import TestData, NaverWebtoon, NaverWebnovel, DaumWebtoon, Netflix

# Create your views here.

def home(request):
    return render(request, 'main.html')

def result(request):
    input_val = request.POST['input_val']
    # 
    result_data = NaverWebtoon.objects.filter(intro__contains = input_val)
    # print('💜', result_data.count())
    count = result_data.count()

    context = {
        'result_data' : result_data
    }

    # if count == 0 :
    #     context = {
    #         'result_data' : result_data,
    #         'msg' : '데이터가 없습니다. '
    #     }
    #     # print("💜")
    # else :
    #     context = {
    #         'result_data' : result_data
    #     }
    return render(request, 'test.html', context)