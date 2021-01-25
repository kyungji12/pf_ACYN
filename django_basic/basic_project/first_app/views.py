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

def add(request, class_pk):
    class_obj = AiClass.objects.get(pk=class_pk)
    
    if request.method == 'POST':
        AiStudent.objects.create(participate_class = class_obj,
                                 name=request.POST['name'],
                                phone_num = request.POST['phone_num'],
                                intro = request.POST['intro'],
                                interest=request.POST['interest']
                                )
        return redirect('detail', class_pk)
    
    context = {'class_obj' : class_obj}
    return render(request, 'add.html', context)

def edit(request, student_pk):
    if request.method == "POST":
        target_student = AiStudent.objects.filter(pk = student_pk)
        #update하려면 filter로 해야함
        target_student.update(name=request.POST['name'],
                            phone_num = request.POST['phone_num'],
                            intro = request.POST['intro'],
                            interest=request.POST['interest']
                            )

        # class_room = AiStudent.objects.get(pk = student_pk).participate_class.class_num
        # print('💜', class_room)
        # return redirect('detail', class_room)
        return redirect('student', student_pk)

    student = AiStudent.objects.get(pk=student_pk)
    context = {'student': student}
    return render(request, 'edit.html', context)

def student(request, student_pk):
    target_student = AiStudent.objects.get(pk = student_pk)
    class_num = target_student.participate_class.class_num
    # print('🌷', target_student.name)
    context = { 
        'student' : target_student,
        'class_num' : class_num
    }
    return render(request, 'student.html', context)

def delete(request, class_num, student_pk):
    target_student = AiStudent.objects.get(pk = student_pk)
    target_student.delete()

    class_pk = class_num

    return redirect('detail', class_pk)

# 에러메세지 모음
ERROR_MSG = {
    'ID_EXIST': '이미 존재하는 아이디입니다.',
    'ID_NOT_EXIST': '존재하지 않는 아이디입니다.',
    'ID_PW_MISSING': '아이디와 비밀번호를 확인해주세요.',
    'PW_CHECK': '비밀번호가 일치하지 않습니다.'
}

def signup(request):

    context = {
        'error' : {
            'state' : False,
            'msg' : ''
        },
    }
    if request.method == 'POST':
        #input값 미리 변수처리
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_pw_check = request.POST['user_pw_check']

        # class_num = int(request.POST['class_num'])
        # participate_class = AiClass.objects.get(class_num = class_num)
        # name = request.POST['name']
        # phone_num = request.POST['phone_num']

        # AiStudent.objects.create(
        #     participate_class=participate_class,
        #     user = created_user,
        #     name = name,
        #     phone_num = phone_num
        #     )
        
        if (user_id and user_pw) :
            user = User.objects.filter(username=user_id)

            if len(user) == 0 : #존재하지 않는 아이디
                if user_pw == user_pw_check: #비밀번호 일치하는지 
                    created_user = User.objects.create_user( #최종 회원가입
                        username=user_id,
                        password=user_pw
                    )
                    #최종 로그인
                    auth.login(request, created_user)
                    return redirect('main')
                else : # 비밀번호가 일치하지 않습니다.
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else : # 이미 존재하는 아이디입니다. 
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_EXIST']
        else : #아이디와 비밀번호를 확인해주세요
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'signup.html', context)

def login(request):

    context = {
        'error' : {
            'state' : False,
            'msg' : ''
        },
    }
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']

        user = User.objects.filter(username=user_id)

        if (user_id and user_pw): #아이디 비번 입력
            if len(user) != 0:
                user = auth.authenticate(
                    username=user_id,
                    password=user_pw
                )
            if user != None :
                auth.login(request, user)
                return redirect('main')
            else : #비밀번호 불일치
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['PW_CHECK']
        else: #아이디 잘못 입력 or 존재하지 않음
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_NOT_EXIST']
    else: #아이디 비번 입력해주세요
        context['error']['state'] = True
        context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('main')
