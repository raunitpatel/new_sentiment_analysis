from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




def LoginPage(request):
    if request.user.is_authenticated:   
        return redirect('dashboard')
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'login.html')

    return render(request, 'login.html')


def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if (request.method == 'POST'):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # print(username, email, password1, password2)
        if (User.objects.filter(username=username).exists()):
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
        if (password1 == password2):
            my_user = User.objects.create_user(username, email, password1)
            my_user.save()
            return redirect('login')
        else:
            messages.error(request, 'Password not matched')
            return render(request, 'register.html')

    return render(request, 'register.html')





@login_required(login_url='login')
def AccountPage(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        messages.success(
            request, 'Your profile has been updated successfully.')
        return redirect('account')

    else:
        context = {
            'user': user,
        }
        return render(request, 'account.html', context)


@login_required(login_url='login')
def PasswordPage(request):
    if request.method == 'POST':
        current_password = request.POST.get('password1')
        new_password = request.POST.get('password2')
        confirm_password = request.POST.get('password3')

        user = request.user
        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return render(request, 'password.html')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return render(request, 'password.html')

        user.set_password(new_password)
        user.save()
        user = authenticate(username=user.username, password=new_password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Password updated successfully.')
            return redirect('account')
        else:
            messages.error(request, 'There was an error re-authenticating. Please log in again.')
            return redirect('login')

    return render(request, 'password.html')


@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    return redirect('home')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)