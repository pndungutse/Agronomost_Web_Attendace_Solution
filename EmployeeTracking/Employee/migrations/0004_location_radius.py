# Generated by Django 3.2 on 2021-06-05 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0003_attendence_agr'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='radius',
            field=models.FloatField(blank=True, default=100.0, null=True, verbose_name='Radius'),
        ),
    ]
