from django.shortcuts import render #html파일에 원하는 context인자를 보낼 수 있음
from django.shortcuts import redirect #url만 이동하는 것

# Create your views here.
def home(request):
    return render(request, 'home.html')

def desc(request):
    return render(request, 'desc.html')

def workout(request):
    return render(request, 'workout.html')

def result(request):
    return render(request, 'result.html')




def video_test(request):
    return render(request, 'video_test.html')

def video_test2(request):
    return render(request, 'video_test2.html')