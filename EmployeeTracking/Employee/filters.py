import django_filters
from django_filters import CharFilter
from django.db.models import Q
import django_filters
from django_filters import DateFilter
from .models import *

class AttendanceFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr="gte")
    end_date = DateFilter(field_name="date_created", lookup_expr="lte")
    
    class Meta:
        model = Attendence_Agr
        fields = '__all__'
        exclude = ['agronomist','curr_latitude', 'curr_longitude', 'date_created']
      
        
class AgronomistFilter(django_filters.FilterSet):
    search = CharFilter(method='Agronomist_custom_filter' ,field_name='search', label='')

    class Meta:
        model = Agronomist
        fields = ['search']

    def Agronomist_custom_filter(self, queryset, name, value):
        return Agronomist.objects.filter(
            Q(agr_code__icontains=value) | Q(first_name__icontains=value) | Q(last_name__icontains=value) |Q(phone__icontains=value) | Q(email__icontains=value)).order_by("id")
        
