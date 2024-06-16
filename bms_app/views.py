from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect,get_object_or_404

from django.db.models import Q

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt

from .models import (Bus,
                     Booking,
                     Seat)
import json
import random

from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import UserSerializer, BusSerializer, SeatSerializer, BookingSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def index(request):
    b= Bus.objects.all()
    user=request.User
    context = {
        'b':b,
        'user':user
    }
    return render(request, 'index.html',context)

@login_required
def bus_list(request):
    query = request.GET.get('q')
    if query:
        buses = Bus.objects.filter(Q(start_point__name__icontains=query) | Q(start_point__address__icontains=query))
    else:
        buses = Bus.objects.all()
    return render(request, 'bus_list.html', {'buses': buses})

@login_required
def book_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    Booking.objects.create(user=request.user, bus=bus)
    return redirect('booking_confirmation', bus_id=bus.id)

@login_required
def select_seat(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    seats = list(Seat.objects.filter(bus=bus).values('id','seat_number','is_occupied'))
    seats = json.dumps(seats)
    # print(seats)

    return render(request, 'select_seat.html', {'bus': bus, 'seats': seats})

@csrf_exempt
def confirm_seat(request):
    if request.method=='POST':
        data=json.loads(request.body)
        seats_ids=data.get('seats',[])
        bus_id=data.get('bus_id')

        Seat.objects.filter(id=seats_ids,bus__id=bus_id).update(is_occupied=True)
 

        #generating a rand num
        # ticket_number=random.randint(100000,999999)
        # print({random.randint})
        return JsonResponse({'ticket_number':'success'})
    
    return JsonResponse({'error':'Invalid request'},status=400)



@login_required
def book_seat(request, bus_id, seat_id):
    bus = get_object_or_404(Bus, id=bus_id)
    seat = get_object_or_404(Seat, id=seat_id)
    if seat.is_occupied:
        return redirect('select_seat', bus_id=bus.id)
    Booking.objects.create(user=request.user, bus=bus, seat=seat)
    seat.is_occupied = True
    seat.save()
    return redirect('booking_confirmation', bus_id=bus.id, seat_id=seat.id)

@login_required
def booking_confirmation(request, bus_id, seat_id):
    bus = get_object_or_404(Bus, id=bus_id)
    seat = get_object_or_404(Seat, id=seat_id)
    # import pdb; pdb.set_trace()
    return render(request, 'booking_confirmation.html', {'bus': bus, 'seat': seat})

@csrf_exempt
def reset_seats(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            bus_id = data.get('bus_id')
            seat_ids = data.get('seats')

            if not bus_id or not seat_ids:
                return JsonResponse({'status': 'fail', 'message': 'Invalid data'}, status=400)

            seats = Seat.objects.filter(id__in=seat_ids, bus_id=bus_id)
            seats.update(is_occupied=False)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'fail', 'message': 'Invalid method'}, status=400)

@login_required
def booking_history(request, bus_id):
    user = request.user
    bookings= Seat.objects.filter(bus__id=bus_id,is_occupied=True)
    # bookings = Booking.objects.filter(user=user, bus_id=bus_id).select_related('bus', 'seat', 'user')
    # for booking in bookings:
    #     print(f'Booking: Bus {booking.bus.number}, Seat {booking.seat.seat_number}, Date {booking.date_booked}')
    print(bookings)
    return render(request, 'booking_history.html', {'bookings': bookings})

#User
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully. You can now log in.')
            return redirect('bus_list')
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
            return redirect('bus_list') 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')