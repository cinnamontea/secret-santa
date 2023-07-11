from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from accounts.forms import CustomUserCreationForm, LoginForm


def register_view(request, *args, **kwargs):
    user = request.user

    if user.is_authenticated:
        return redirect('home_feed')
    
    context = {}
    if request.POST:

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Since the form is a 'UserCreationForm', saving it saves the underlying user (if it's valid).
            form.save()
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect('home_feed')
        
        else:
            context['registration_form'] = form

    return render(request, 'accounts/register.html', context)


def login_view(request, *args, **kwargs):
    user = request.user

    if user.is_authenticated:
        return redirect('home_feed')
    
    context = {}
    if request.POST:

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password']
            user = authenticate(username=username, password=raw_password)

            if user:
                login(request, user)
                return redirect('home_feed')
        
        else:
            context['login_form'] = form
    
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('home_feed')
    
