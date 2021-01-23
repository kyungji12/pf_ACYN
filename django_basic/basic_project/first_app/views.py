from django.shortcuts import render
# from django.http import HttpResponse
from django.shortcuts import redirect
from .models import AiClass, AiStudent
from django.contrib.auth.models import User
from django.contrib import auth #login logout정보 들어있음

# Create your views here.

# def home(request):
#     return HttpResponse('Hello World!!')
# def home(request):
#     return render(request, 'home.html')

def main(request):
    ai_class = AiClass.objects.all() #데이터 가져오기
    
    context = {'ai_class':ai_class} #가져온 데이터 객체에 담기

    return render(request, 'main.html', context) #객체에 담은 데이터 화면에 뿌리기

def detail(request, class_pk):
    # print('⭐️⭐️⭐️⭐️⭐️⭐️',class_pk)
    class_obj = AiClass.objects.get(pk = class_pk) #class_pk인 데이터 가져오기
    student_obj = AiStudent.objects.filter(participate_class=class_pk)

    context = {
        'class_pk' : class_pk,
        'class_obj': class_obj,
        'student_obj' : student_obj
        } #pk 객체에 담기

    return render(request, 'detail.html',context)

# def student(request, student_pk):
#     student = AiStudent.objects.get(pk = student_pk)

#     context = {'student':student}

#     return render(request, 'student.html', context)

def add(request, class_pk):
    class_obj = AiClass.objects.get(pk=class_pk)
    
    if request.method == 'POST':
        AiStudent.objects.create(participate_class = class_obj,
                                 name=request.POST['name'],
                                phone_num = request.POST['phone_num'])
        return redirect('detail', class_pk)
    
    context = {'class_obj' : class_obj}
    return render(request, 'add.html', context)

def edit(request, student_pk):
    #get(pk)는 object만 반환, filter는 queryset자체를 반환
    student_obj = AiStudent.objects.filter(pk=student_pk)
    print('🍀',student_obj)
    #return redirect('detail', class_pk)