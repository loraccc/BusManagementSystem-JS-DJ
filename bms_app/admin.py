from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register (Bus)
admin.site.register (Destination)
admin.site.register (PickupPoint)
admin.site.register (Seat)
admin.site.register (Booking)