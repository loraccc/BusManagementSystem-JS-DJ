# Generated by Django 5.0.6 on 2024-06-18 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms_app', '0007_alter_booking_seat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bus',
            options={'permissions': [('edit_bus', 'Can edit bus'), ('reset_seats', 'Can reset seats')]},
        ),
    ]
