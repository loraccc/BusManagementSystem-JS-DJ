# Generated by Django 5.0.6 on 2024-06-12 07:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bms_app', '0003_bus_seats_bus_ticket_price_seat_booking_seat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='bus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seat', to='bms_app.bus'),
        ),
    ]
