from django.shortcuts import render


def register_page(request):
    return render(request, "api/register.html")

def quiz_page(request):
    return render(request, 'api/quiz.html')

def landing_page(request):
    return render(request, "api/base.html")

def login_page(request):
    return render(request, "api/login.html")


def class New:
    
