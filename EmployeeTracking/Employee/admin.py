from django.contrib import admin
from .models import Agronomist, Staff,Location, Agronomist_location, Attendence_Agr


admin.site.register(Agronomist),
admin.site.register(Staff),
admin.site.register(Location),
admin.site.register(Agronomist_location)
admin.site.register(Attendence_Agr)


