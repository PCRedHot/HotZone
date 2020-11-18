from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def loginView(request):
    wrong = False
    data = request.GET
    if 'result' in data:
        if data['result'] == 'fail':
            wrong = True
    return render(request, 'login.html', {'isLoginFailed': wrong})

def loginAttemptView(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/login?result=fail')

@login_required
def logoutView(request):
    logout(request)
    return redirect('/login')
