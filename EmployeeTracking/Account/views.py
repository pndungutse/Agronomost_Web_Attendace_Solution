from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from Employee.decorator import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from Account.forms import CreateUserForm
from django.contrib import messages
from Employee.models import Agronomist, Staff
from Employee.models import Agronomist, Staff, Location, Agronomist_location, Attendence_Agr
import datetime

# Create your views here.

success = 'Success!'
error = 'Error!'
error_message = 'Something Wrong Happened, please Try Again'

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def homeStaff(request):
    no_agronomists = Agronomist.objects.all().count()
    no_locations = Location.objects.all().count()
    no_agr_loc = Agronomist_location.objects.all().count()
    
    year1 =datetime.datetime.now().year
    print(year1)
    january = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=1).count() *100)/(40*no_agronomists))
    february = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=2).count() *100)/(40*no_agronomists))
    march = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=3).count() *100)/(40*no_agronomists))
    april = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=4).count() *100)/(40*no_agronomists))
    may = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=5).count() *100)/(40*no_agronomists))
    june = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=6).count() *100)/(40*no_agronomists))
    july = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=7).count() *100)/(40*no_agronomists))
    august = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=8).count() *100)/(40*no_agronomists))
    september = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=9).count() *100)/(40*no_agronomists))
    october = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=10).count() *100)/(40*no_agronomists))
    november = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=11).count() *100)/(40*no_agronomists))
    december = ((Attendence_Agr.objects.filter(date_created__year__gte=2021, date_created__month=12).count() *100)/(40*no_agronomists))
    
    context = {'no_agronomists':no_agronomists,'no_locations':no_locations,'no_agr_loc':no_agr_loc,
               'january':january,'february':february,'march':march, 'april':april, 'may':may, 'june':june,
               'july':july,'august':august,'september':september,'october':october, 'november':november, 'december':december}
    return render(request, 'Employee/adminPages/homeStaff.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + username)
            return redirect('loginPage')
    context = {'form':form}
    return render(request, 'accounts/register.html', context)
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if Staff.objects.filter(user=user):
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('homeStaff')
            elif Agronomist.objects.filter(user=user):
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('homeAgronomist')               
    else:
        form = AuthenticationForm()
    context={'form':form}
    return render(request, 'accounts/login.html', context)
def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginPage')
    
def View401(request):
    
    context = {}
    return render(request, '401.html', context)


