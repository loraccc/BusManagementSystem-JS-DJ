from rest_framework import serializers
from .models import User, Bus, Seat, Booking

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']

class BusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bus
        fields = ['url', 'number', 'route']

class SeatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seat
        fields = ['url', 'seat_number', 'bus']

class BookingSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    bus = serializers.HyperlinkedRelatedField(
        view_name='bus-detail',
        queryset=Bus.objects.all()
    )
    seat = serializers.HyperlinkedRelatedField(
        view_name='seat-detail',
        queryset=Seat.objects.all()
    )

    class Meta:
        model = Booking
        fields = ['url', 'user', 'bus', 'seat', 'date_booked']
