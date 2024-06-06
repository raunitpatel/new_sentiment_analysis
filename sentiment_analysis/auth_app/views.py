from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def HomePage(request):
    return render(request, 'home.html')

def LoginPage(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'login.html')

    return render(request, 'login.html')

def RegisterPage(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # print(username, email, password1, password2)
        if(User.objects.filter(username=username).exists()):
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
        if(password1 == password2):
            my_user = User.objects.create_user(username, email, password1)
            my_user.save()
            return redirect('login')
        else:
            messages.error(request, 'Password not matched')
            return render(request, 'register.html')




    return render(request, 'register.html')

@login_required(login_url='login')
def DashboardPage(request):
    return render(request, 'dashboard.html')
def AboutPage(request):
    return render(request, 'about.html')
def AccountPage(request):
    return render(request, 'account.html')
def PasswordPage(request):
    return render(request, 'password.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')
