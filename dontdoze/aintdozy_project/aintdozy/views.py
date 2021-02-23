from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'main.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def about(request):
    return render(request, 'about.html')

def detect(request):
    return render(request, 'detect.html')

def alarm(request):
    return render(request, 'alarm.html')