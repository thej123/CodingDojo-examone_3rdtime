from django.shortcuts import render, redirect
from models import *
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, 'examv3/index.html')

def main(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['id'])
    }
    return render(request, 'examv3/main.html', context)

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for x in result:
            messages.error(request, x)
        return redirect('/')
    else:
        request.session['id'] = result.id
        messages.success(request, 'You have registered successfully!')
        return redirect('/examv3/main')
    
def login(request):
    print 'hello 2'
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for x in result:
            messages.error(request, x)
        return redirect('/')
    else:
        request.session['id'] = result.id
        messages.success(request, 'You have logged in!')
        return redirect('/examv3/main')

def logout(request):
    request.session.clear()
    return redirect('/')