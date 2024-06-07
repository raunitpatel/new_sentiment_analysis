"""sentiment_analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from auth_app import views as auth_views
from analysis import views as analysis_views

handler404 = 'auth_app.views.custom_404_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', analysis_views.HomePage, name='home'),
    path('login/', auth_views.LoginPage, name='login'),
    path('register/', auth_views.RegisterPage, name='register'),
    path('dashboard/', analysis_views.DashboardPage, name='dashboard'),
    path('logout/', auth_views.LogoutPage, name='logout'),
    path('about/', analysis_views.AboutPage, name='about'),
    path('account/', auth_views.AccountPage, name='account'),
    path('password/', auth_views.PasswordPage, name='password'),
    path('news-sentiment/', analysis_views.HomePage, name='news-sentiment'),
]
