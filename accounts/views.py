from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm

User = get_user_model()

"""Функция для авторизации"""


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


"""Функция выхода"""


def logout_view(request):
    logout(request)
    return redirect('home')
