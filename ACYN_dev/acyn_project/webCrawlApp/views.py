from django.shortcuts import render #html파일에 원하는 context인자를 보낼 수 있음
from django.shortcuts import redirect #url만 이동하는 것

# from django.http import HttpResponse
from .models import TestData, NaverWebtoon, NaverWebnovel, DaumWebtoon, Netflix

# Create your views here.

def home(request):
    return render(request, 'main.html')

def result(request):
    # context = {
    #     'error' : {
    #         'state' : False, 
    #         'mgs' : ''
    #     }
    # }

    # input_val = request.POST['input_val']
    # print("🥲", input_val)

    test_data = NaverWebtoon.objects.all() #데이터 가져오기
    
    context = {
        'testDT' : test_data
    }

    # (입력한 단어가 있을 때 -> 데이터 안에 있을 때 vs 없을 때) vs (없을 때)
    # if input_val = request.POST['input_val']:
    #     title = 
    
    # else : 

    # context = {
    #     'input_val' : input_val
    # }
    # return render(request, 'result.html', context)
    return render(request, 'test.html', context)