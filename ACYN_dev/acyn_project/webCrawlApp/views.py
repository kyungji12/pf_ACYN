from django.shortcuts import render #html파일에 원하는 context인자를 보낼 수 있음
from django.shortcuts import redirect #url만 이동하는 것

# from django.http import HttpResponse
from .models import TestData, NaverWebtoon, NaverWebnovel, DaumWebtoon, Netflix

# Create your views here.

def home(request):
    return render(request, 'main.html')

def result(request):
    input_val = request.POST['input_val']
    # print("🥲", input_val)
    context = {
        'input_val' : input_val
    }
    return render(request, 'result.html', context)