from django.urls import path
from Employee.views import homeAgronomist

urlpatterns = [
    path('', homeAgronomist, name='homeAgronomist'),    
]