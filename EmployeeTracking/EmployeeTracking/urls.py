"""EmployeeTracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from Employee.views import *
from Account.views import logoutUser, loginPage, registerPage, View401, homeStaff

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginPage, name='loginPage'),
    path('register', registerPage, name='registerPage'),
    path('agronomist/', include('Employee.urls')),
    # path('homeEmployee', homeEmployee, name='homeEmployee'),
    path('homeStaff', homeStaff, name='homeStaff'),
    path('agronomists', agronomistList, name='agronomists'),
    path('addAgronomist', addAgronomist, name='addAgronomist'),
    path('logoutUser', logoutUser, name='logoutUser'),
    path('View401', View401, name='View401'),
    path('makeAttendance', makeAttendance, name='makeAttendance'),
    path('viewYourAttendances', viewYourAttendances, name='viewYourAttendances'),
    path('attendanceReports',attendanceReports,name='attendanceReports'),
    path('makeAttendanceStaff', makeAttendanceAdmin, name='makeAttendanceStaff'),
    path('viewAttendancesStaff', viewAttendancesAdmin, name='viewAttendancesStaff'),
    path('attendanceReportsStaff',attendanceReportsAdmin, name='attendanceReportsStaff'),
    path('locations', locations, name='locations'),
    path('add_location',add_location, name='add_location'),
    path('location_update/<str:pk_location>',location_update,name='location_update'),
    path('location_delete/<str:id>', location_delete, name='location_delete'),
    path('assignLocation', assignLocation, name='assignLocation'),
    path('newAssignLocation', newAssignLocation, name='newAssignLocation'),
    path('updateAssignLocation/<str:pk_agr_loc>', updateAssignLocation, name='updateAssignLocation'),
    path('agr_location_delete/<str:id>', agr_location_delete, name='agr_location_delete'),
    path('saveAttendance', saveAttendance, name='saveAttendance'),
    path('failed', attendanceFailed, name='failed'),
    path('allAgronomistPDF', allAgronomistPDF, name='allAgronomistPDF'),
    path('allLocationsPDF',allLocationsPDF,name='allLocationsPDF'),
    path('agr_locPDF', agronomist_locationPDF, name='agr_locPDF')
    
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

