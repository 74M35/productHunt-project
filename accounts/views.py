from django.shortcuts import render

def signup(request):
    render(request, 'accounts/signup.html')

def login(request):
    render(request, 'accounts/login.html')

def logout(request):
    # change to homepage
    render(request, 'accounts/signup.html')