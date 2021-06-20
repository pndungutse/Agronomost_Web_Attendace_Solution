# Generated by Django 3.2 on 2021-06-08 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0004_location_radius'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendence_agr',
            name='attendance_type',
            field=models.CharField(choices=[('CHECK_IN', 'CHECK_IN'), ('CHECK_OUT', 'CHECK_OUT')], default='CHECK_IN', max_length=15),
        ),
    ]
