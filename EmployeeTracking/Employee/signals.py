from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Agronomist, Staff
from django.contrib.auth.models import Group


def employee_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='agronomist')
        instance.groups.add(group)
        
        Agronomist.objects.create(
            user=instance,
            first_name=instance.username,
        )
        print('Agronomist created')
        
post_save.connect(employee_profile, sender=User)
        
        
        
         
 