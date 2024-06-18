from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser

    
class PickupPoint(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.address}"

class Destination(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.address}"

class Bus(models.Model):
    number = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='bus_photos/', blank=True, null=True)
    start_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, related_name='start_point')
    end_point = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='end_point')
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    seats = models.PositiveIntegerField(default=40)  
    class Meta:
        permissions = [
                    ('edit_bus', 'Can edit bus'),
                    ('reset_seats', 'Can reset seats'),
                ]

    def __str__(self):
        return self.number

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='seatss')
    seat_number = models.PositiveIntegerField()
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f'Bus {self.bus.number} - Seat {self.seat_number}'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE,related_name='buss')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE,default=0,related_name='booking')
    date_booked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking by {self.user.username} for bus {self.bus.number}, seat {self.seat.seat_number}'
    
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f'{self.user.username} Profile'