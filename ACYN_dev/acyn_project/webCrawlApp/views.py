from django.shortcuts import render #html파일에 원하는 context인자를 보낼 수 있음
from django.shortcuts import redirect #url만 이동하는 것

# from django.http import HttpResponse
from .models import TestData, NaverWebtoon, NaverWebnovel, DaumWebtoon, Netflix

# Create your views here.

def home(request):
    return render(request, 'main.html')

def result(request):
    input_val = request.POST['input_val']

    naver_wt = NaverWebtoon.objects.filter(intro__contains = input_val)
    naver_nv = NaverWebnovel.objects.filter(intro__contains = input_val)
    daum_wt = DaumWebtoon.objects.filter(intro__contains = input_val)
    netflix = Netflix.objects.filter(intro__contains = input_val)

    result_data = {
        'naver_wt' : naver_wt,
        'naver_nv' : naver_nv,
        'daum_wt' : daum_wt,
        'netflix' : netflix
    }

    # print('💜', result_data.count())
    context = {
        'error' : {
            'state' : False,
            'msg' : ''
        },
        'result_data' : result_data
    }

    if input_val : #입력값이 있다면
        if not result_data : #일치하는 값이 없다면 
            context['error']['state'] = True
            context['error']['msg'] = '찾으시는 컨텐츠가 없습니다.'
            return render(request, 'result.html', context)
        else : #일치하는 값이 있다면
            return render(request, 'result.html', context)

    else : #입력값이 없다면
        context['error']['state'] = True
        context['error']['msg'] = '검색어를 입력해주세요.'
        
        return render(request, 'main.html', context)
