from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point, GEOSGeometry
from django.db import models


# Create your models here.
ATTENDANCE_TYPE = [
    ("CHECK_IN", "CHECK_IN"),
    ("CHECK_OUT", "CHECK_OUT"),
]

class Agronomist(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    agr_code = models.CharField(max_length=5, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=30)
    profile_pic = models.ImageField(default='anonymous-user.png', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return '%s %s' %(self.first_name, self.last_name)
    
class Staff(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=30)
    profile_pic = models.ImageField(default='anonymous-user.png',null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.first_name
    

class Location(models.Model):
    place_name = models.CharField(blank=True,max_length=255)
    latitude = models.FloatField(blank=True, null=True, verbose_name='Latitude')
    longitude = models.FloatField(blank=True, null=True, verbose_name='Longitude')
    radius = models.FloatField(blank=True, null=True, verbose_name='Radius', default=100.00)

    def __str__(self):
        return self.place_name
    
class Agronomist_location(models.Model):
    agronomist = models.ForeignKey(Agronomist,on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s - %s' %(self.agronomist.first_name, self.location.place_name)
    
class Attendence_Agr(models.Model):
    agronomist = models.ForeignKey(Agronomist, on_delete=models.CASCADE)
    attendance_type = models.CharField(max_length=15, choices=ATTENDANCE_TYPE, default="CHECK_IN")
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return '%s - %s' %(self.agronomist.first_name, self.date_created) 
    
    
    
    