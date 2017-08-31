from django.shortcuts import render, redirect
from models import *
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, 'examv3/index.html')

def travels(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['id']),
        'own_trips' : Trip.objects.filter(trip_joiners=User.objects.get(id=request.session['id'])),
        'other_trips' : Trip.objects.exclude(trip_joiners=User.objects.get(id=request.session['id']))
    }
    return render(request, 'examv3/travels.html', context)

def travels_add(request):
    return render(request, 'examv3/add.html')

def destination(request, trip_id):
    context = {
        'trip' : Trip.objects.get(id=trip_id),
        'trip_joiners' : User.objects.filter(trips_goingto__id=trip_id).exclude(trip_created__id=trip_id),
    }
    return render(request, 'examv3/destination.html', context)

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for x in result:
            messages.error(request, x)
        return redirect('/')
    else:
        request.session['id'] = result.id
        messages.success(request, 'You have registered successfully!')
        return redirect('/examv3/travels')
    
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
        return redirect('/examv3/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

def home(request):
    return redirect('/examv3/travels')

def add_trip(request):
    result = Trip.objects.validate_trip(request.POST)
    # checking for validation errors
    if len(result) > 0:
        for x in result:
            messages.error(request, x)
        return redirect('/examv3/travels/add')
    # creating trip object
    Trip.objects.create(
        destination=request.POST['destination'],
        description=request.POST['description'],
        travel_date_from=request.POST['travel_date_from'],
        travel_date_to=request.POST['travel_date_to'],
        trip_creater=User.objects.get(id=request.session['id'])
        )
    # creating many-many relationship between the trip and user objects
    Trip.objects.get(
        destination=request.POST['destination'], 
        description=request.POST['description'], 
        travel_date_from=request.POST['travel_date_from'],
        travel_date_to=request.POST['travel_date_to'],
        trip_creater=User.objects.get(id=request.session['id'])
        ).trip_joiners.add(User.objects.get(id=request.session['id']))
    
    return redirect('/examv3/travels')

def join_trip(request, trip_id):
    Trip.objects.get(id=trip_id).trip_joiners.add(User.objects.get(id=request.session['id']))
    return redirect('/examv3/travels')
