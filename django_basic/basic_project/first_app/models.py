from django.db import models
# from django.contrib.auth.models

# Create your models here.
class AiClass(models.Model):
    class_num = models.IntegerField()
    lecturer = models.CharField(max_length=30)
    class_room = models.CharField(max_length=30)
    student_num = models.IntegerField()

class AiStudent(models.Model):
    # 학생 테이블
    class_num = models.IntegerField()  # fk로 class 테이블 pk받아오기
    name = models.CharField(max_length=10)  #학생이름
    phone_num = models.CharField(null=True, max_length=20)  #연락처
    # intro = models.CharField(null=True, max_length=100)  #자기소개
    # interest = models.CharField(null=True, max_length=50)  #관심사

############################################################
# 1 : N 구조
# 매번 class_num을 pk로 넘겨줄 필요없게 만들어
# models.ForeignKey() 를 이용해 class와의 관계
# models.ForeignKey(어떤테이블을 참조할 것인지 A , on_delete=(options), related_name = '')
# on_delete : 만약 참조하는 테이블A가 사라지면 지금 테이블은 어떻게 할것인가요?
# -> models.CASCADE : 참조테이블이 사라지면 지금 테이블도 삭제
#       ex ) 글 - 댓글관계 : 글이 삭제되면 댓글도 전부 삭제된다
# -> models.SET_NULL : 참조하는 테이블이 사라지면 Null값을 넣어줘
# related_name : 참조하는 테이블에서 ForeignKey로 엮여있는 테이블을 지칭하는 이름은?
#  ★헷갈리지말자 : -> AiClass 테이블에서 AiStudent테이블을 어떻게 부를 것인지 !
#     ex) class_obj.student.all -> student라고 불리는 AiStudent테이블에서 all가져와라
############################################################

# class AiStudent(models.Model) :
#     participate_class = models.ForeignKey(AiClass, 
#     on_delete=models.CASCADE, related_name='student')

#     #학생테이블
#     user = models.OneToOneField(User, on_delete=models.CASCADE,
#     related_name='student')
#     # class_num = models.IntegerField()  # fk로 class 테이블 pk받아오기
#     name = models.CharField(max_length=10)  #학생이름
#     phone_num = models.CharField(null=True, max_length=20)  #연락처
#     # intro = models.CharField(null=True, max_length=100)  #자기소개
#     # interest = models.CharField(null=True, max_length=50)  #관심사