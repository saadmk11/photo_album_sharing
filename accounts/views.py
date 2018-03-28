from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import UserLoginForm, SignUpForm


def login_view(request):
    '''users will login with their Username & Password'''
    if request.user.is_authenticated():
        return redirect('album:index')
    else:

        form = UserLoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # authenticates username & Password
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('album:index')

        context = {
            'title': 'Login',
            'form': form
        }

    return render(request, "accounts/form.html", context)


def logout_view(request):
    '''logs out the logged in users'''
    if not request.user.is_authenticated():
        # if not loggged in takes user to login page.
        return redirect('accounts:login')
    else:
        logout(request)
        return redirect('album:index')


def register_view(request):
    '''Users will Create an Account.'''
    if request.user.is_authenticated():
        return redirect('album:index')
    else:
        form = SignUpForm(request.POST or None)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # authenticates username & Password
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('album:index')

        context = {
            'title': 'Register',
            'form': form
        }

    return render(request, 'accounts/form.html', context)
