import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils  import render_to_pdf
from django.template.loader import get_template
from django.core.paginator import Paginator
from .decorator import unauthenticated_user, allowed_users
from .utils import render_to_pdf
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Agronomist, Staff, Location, Agronomist_location, Attendence_Agr
from .forms import Agronomist_locationForm, LocationForm, Attendence_AgrForm, AgronomistForm
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .filters import AgronomistFilter
from .filters import AttendanceFilter
import sweetify
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
success = 'Success!'
error = 'Error!'
error_message = 'Something Wrong Happened, please Try Again'

# @login_required(login_url='loginPage')
# @allowed_users(allowed_roles=['staff'])
# def homeStaff(request):
#     no_agronomists = Agronomist.objects.all().count()
#     no_locations = Location.objects.all().count()
#     no_agr_loc = Agronomist_location.objects.all().count()
    
#     year1 =datetime.datetime.now().year
#     print(year1)
#     january = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=1).count() *100)/(40*no_agronomists))
#     february = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=2).count() *100)/(40*no_agronomists))
#     march = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=3).count() *100)/(40*no_agronomists))
#     april = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=4).count() *100)/(40*no_agronomists))
#     may = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=5).count() *100)/(40*no_agronomists))
#     june = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=6).count() *100)/(40*no_agronomists))
#     july = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=7).count() *100)/(40*no_agronomists))
#     august = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=8).count() *100)/(40*no_agronomists))
#     september = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=9).count() *100)/(40*no_agronomists))
#     october = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=10).count() *100)/(40*no_agronomists))
#     november = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=11).count() *100)/(40*no_agronomists))
#     december = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=12).count() *100)/(40*no_agronomists))
    
#     context = {'no_agronomists':no_agronomists,'no_locations':no_locations,'no_agr_loc':no_agr_loc,
#                'january':january,'february':february,'march':march, 'april':april, 'may':may, 'june':june,
#                'july':july,'august':august,'september':september,'october':october, 'november':november, 'december':december}
#     return render(request, 'Employee/adminPages/homeStaff.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['agronomist'])
def homeAgronomist(request):
    
    user = request.user
    agronomist = Agronomist.objects.get(user=user)
    last_week = datetime.today() - timedelta(days=7)
    last_2_week = datetime.today() - timedelta(days=14)
    last_3_week = datetime.today() - timedelta(days=21)
    last_4_week = datetime.today() - timedelta(days=30)
    
    week1 = (Attendence_Agr.objects.filter(agronomist=agronomist, date_created__gte=last_week).count()* 100)/14
    week2 = (Attendence_Agr.objects.filter(agronomist=agronomist, date_created__gte=last_2_week).count()* 100)/28
    week3 = (Attendence_Agr.objects.filter(agronomist=agronomist, date_created__gte=last_3_week).count()*100)/42
    week4 = (Attendence_Agr.objects.filter(agronomist=agronomist, date_created__gte=last_4_week).count()*100)/60

    context = {'week1':week1, 'week2':week2, 'week3':week3, 'week4':week4}
    return render(request, 'Employee/agronomistPages/homeAgronomist.html', context)

def agronomistList(request):
    agronomist_list = Agronomist.objects.all()
    paginator = Paginator(agronomist_list, 5) # Show 5 contacts per page.
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    context = {'page_obj':page_obj}
    return render(request, 'Employee/adminPages/agronomistList.html', context)

def addAgronomist(request):
    form = AgronomistForm()
    
    if(request.method == "POST"):
        form = AgronomistForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agronomist has been Created Successfully')
            return redirect('agronomistList')
    context = {'form':form}
    return render(request, 'Employee/adminPages/registerAgronomist.html', context)

def makeAttendance(request):
    # sweetify.success(request, 'Message sent', button='Ok', timer=3000)

    user = request.user
    agr_user = Agronomist.objects.get(user=user)
    
    userr = Agronomist_location.objects.filter(agronomist=agr_user).first()
    user_latitude = userr.location.latitude
    user_longitude = userr.location.longitude
    radius = userr.location.radius
    
    # form = Attendence_AgrForm()
    # if(request.method == "POST"):
    #     form = Attendence_AgrForm(request.POST) 
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Attendance has been made successfully')
    #         return redirect('homeAgronomist')
    
    
    context = {'user_latitude':user_latitude,'user_longitude':user_longitude, 'radius':radius}
    return render(request, 'Employee/agronomistPages/makeAttendance.html', context)


def saveAttendance(request):
    user = request.user
    agr_user = Agronomist.objects.get(user=user)
    
    userr = Agronomist_location.objects.filter(agronomist=agr_user).first()
    user_latitude = userr.location.latitude
    user_longitude = userr.location.longitude
    radius = userr.location.radius
    print(radius)
    # attendances = Attendence_Agr.objects.filter(date_created__date=date.today())
    
    
    try:
        status = request.GET.get('status')
        distance = request.GET.get('distance')
    except:
        status = None
        distance = None
        
    if status:
        if distance:
            distanceSearched = distance
            float_distance = float(distanceSearched)
                   
            statusSearched = status  
              
            if float_distance < radius:
                try:
                    Attendence_Agr.objects.get(agronomist=agr_user, date_created__date=date.today(), attendance_type=statusSearched)
                    messages.success(request, 'You have already made attendance') 
                    sweetify.error(request, error, text='Info! You have already made attendance', icon='info', timerProgressBar='true', timer=3000)            
                    return redirect('makeAttendance')
                except ObjectDoesNotExist:
                    Attendence_Agr.objects.create(
                            agronomist = agr_user,
                            attendance_type = statusSearched,
                    )

                
                # return redirect('attendanceSuccess')
            else:
                messages.success(request, 'Failed to make attendence! Bad Location')
                context = {'user_latitude':user_latitude,'user_longitude':user_longitude}
                sweetify.error(request, error, text='Unable to Make Attendence', icon='info', timerProgressBar='true', timer=3000)            
                return redirect('failed')
            
    sweetify.success(request, success, text='You have successfully Made Attendence', icon='success', timerProgressBar='true', timer=3000) 
    return redirect('makeAttendance')
    
def attendanceFailed(request):
     
    user = request.user
    agr_user = Agronomist.objects.get(user=user)
    
    userr = Agronomist_location.objects.filter(agronomist=agr_user).first()
    user_latitude = userr.location.latitude
    user_longitude = userr.location.longitude
    
    context = {'user_latitude':user_latitude, 'user_longitude':user_longitude}     
    return render(request, 'Employee/agronomistPages/attendanceFailed.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['agronomist'])
def viewYourAttendances(request):
    
    user = request.user
    userr = Agronomist.objects.get(user=user)
    attendances = Attendence_Agr.objects.filter(agronomist=userr).order_by('-date_created')
    myFilter = AttendanceFilter(request.GET, queryset=attendances)
    attendances = myFilter.qs
    paginator = Paginator(attendances, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'user':user,'page_obj':page_obj,'myFilter':myFilter}
    
    return render(request, 'Employee/agronomistPages/viewYourAttendances.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['agronomist'])
def attendanceReports(request):
    
    context = {}
    return render(request, 'Employee/agronomistPages/attendancesReports.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['agronomist'])
def weekAgronomistReport(request):
    
    context = {}
    return render(request, 'Employee/agronomistPages/weekAgronomistReport.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def makeAttendanceAdmin(request):
    
    context = {}
    return render(request, 'Employee/adminPages/makeAttendanceAdmin.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def viewAttendancesAdmin(request):
    
    context = {}
    return render(request, 'Employee/adminPages/viewAttendancesAdmin.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def attendanceReportsAdmin(request):
    
    context = {}
    return render(request, 'Employee/adminPages/attendanceReportsAdmin.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def assignLocation(request):
    agr_locations = Agronomist_location.objects.all()
    paginator = Paginator(agr_locations, 5) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj':page_obj}
    return render(request, 'Employee/adminPages/assignLocation.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def newAssignLocation(request):
    form = Agronomist_locationForm()
    
    if(request.method == "POST"):
        form = Agronomist_locationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agronomist has been Assigned Location Successfully')
            return redirect('assignLocation')
    context = {'form':form}
    return render(request,'Employee/adminPages/newAssignLocation.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def updateAssignLocation(request, pk_agr_loc):

    agr_loc = Agronomist_location.objects.get(id=pk_agr_loc)
    form = Agronomist_locationForm(instance=agr_loc)
    if request.method == 'POST':
        form = Agronomist_locationForm(request.POST, instance=agr_loc)
        if form.is_valid:
            form.save()
            messages.success(request, 'Assignment Location to Agronomist has been Updated Successfully')
            return redirect('assignLocation')
    context = {'form':form}
    return render(request, 'Employee/adminPages/newAssignLocation.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def agr_location_delete(request, id):
    agr_loc = Agronomist_location.objects.get(pk=id)
    agr_loc.delete()
    messages.success(request, 'Assignment of location to agronomist has been deleted Successfully')
    return redirect('assignLocation')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def locations(request):
    locations = Location.objects.all()
    paginator = Paginator(locations, 5)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj':page_obj}
    
    return render(request, 'Employee/adminPages/locations.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def add_location(request):
    form = LocationForm()
    if(request.method == "POST"):
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location has been added successfully')
            return redirect('locations')
    context = {'form':form}
    return render(request, 'Employee/adminPages/add_location.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def location_update(request, pk_location):

    location = Location.objects.get(id=pk_location)
    form = LocationForm(instance=location)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid:
            form.save()
            messages.success(request, 'Location has been Updated Successfully')
            return redirect('locations')
    context = {'form':form}
    return render(request, 'Employee/adminPages/add_location.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def location_delete(request, id):
    location = Location.objects.get(pk=id)
    location.delete()
    messages.success(request, 'Location has been deleted Successfully')
    return redirect('locations')

def allAgronomistPDF(request):
    template = get_template('Employee/adminPages/allAgronomistsPDF.html')
    user = request.user
    
    agronomists = Agronomist.objects.all()
    context = {'agronomists':agronomists, 'user':user}
    html = template.render(context)
    pdf= render_to_pdf('Employee/adminPages/allAgronomistsPDF.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "All Agronomist Registered"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def allLocationsPDF(request):
    template = get_template('Employee/adminPages/allLocationsPDF.html')
    user = request.user
    
    locations = Location.objects.all()
    context = {'locations':locations, 'user':user}
    html = template.render(context)
    pdf= render_to_pdf('Employee/adminPages/allLocationsPDF.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "All Locations Registered"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def agronomist_locationPDF(request):
    template = get_template('Employee/adminPages/allAgronomistsWithLocationsPDF.html')
    user = request.user
    agronomist_locations = Agronomist_location.objects.all()
    context = {'agronomist_locations':agronomist_locations, 'user':user}
    html = template.render(context)
    pdf= render_to_pdf('Employee/adminPages/allAgronomistsWithLocationsPDF.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "All Agronomist with his/her Location"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"




