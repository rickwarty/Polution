import os
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from core.forms import SignUpForm, LoginForm, AddState
from django.contrib import messages
from core.models import State, Pollution
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
import pandas as pd

# Home
def home(request):
    posts = State.objects.all()
    context = {
        'posts': posts,
        "home": "current"
    }
    return render(request, 'core/home.html', context)


# about
def about(request):
    return render(request, 'core/about.html', {"about": "current"})


# Contact
def contact(request):
    return render(request, 'core/contact.html', {"contact": "current"})


# dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = State.objects.all()
        user = request.user
        gps = user.groups.all()
        full_name = user.get_full_name()
        context = {
            'posts': posts,
            'fullname': full_name,
            'groups': gps,
            "dashboard": "current"

        }
        return render(request, 'core/dashboard.html', context)
    else:
        return redirect("/login/")


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect("/")


# Signup
def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations Your ID is Created")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()

    context = {
        'form': form,
        "signup": "current"
    }
    return render(request, 'core/signup.html', context)


# Login
def user_login(request):
    # if not request.user.is_authenticated :: means user is not logged in so the else part will be executed
    if not request.user.is_authenticated:
        if request.method == "POST":

            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in Successfuly")
                    return redirect("/")
        else:
            form = LoginForm()
        context = {
            'form': form,
            "login": "current"
        }
        return render(request, 'core/login.html', context)
    else:
        # this will execute when the user is already logged in
        return redirect('/')


# add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddState(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pic = form.cleaned_data['pic']
                pst = State(title=title, desc=desc, pic=pic)
                pst.save()
                messages.success(request, "Post is Added Successfully")
                form = AddState()

        else:
            form = AddState()
        img = State.objects.all()
        context = {
            'form': form,
            'img': img
        }
        return render(request, 'core/addpost.html', context)
    else:
        return redirect('/login/')


# update post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = State.objects.get(pk=id)
            form = AddState(request.POST, request.FILES, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, "Post Updated Successfully")

        else:
            pi = State.objects.get(pk=id)
            form = AddState(instance=pi)
        context = {
            'form': form,
            "pi": pi
        }
        return render(request, 'core/updatepost.html', context)
    else:
        return redirect('/login/')


# delete post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = State.objects.get(pk=id)
            pi.delete()
            messages.success(request, "One Post is Deleted")
        return redirect("/dashboard/")
    else:
        return redirect('/login/')


def detailsPost(request, id):
    if request.user.is_authenticated:
        pi = State.objects.get(pk=id)
        return render(request, "core/detail_post.html", {"post": pi})

# os.chdir("C:\\Users\\AQIB\\Downloads\\ML")
# df = pd.read_csv("city_day.csv")
# df1 = df.copy()
# df1['PM2.5']=df1['PM2.5'].fillna((df1['PM2.5'].median()))
# df1['PM10']=df1['PM10'].fillna((df1['PM10'].median()))
# df1['NO']=df1['NO'].fillna((df1['NO'].median()))
# df1['NO2']=df1['NO2'].fillna((df1['NO2'].median()))
# df1['NOx']=df1['NOx'].fillna((df1['NOx'].median()))
# df1['NH3']=df1['NH3'].fillna((df1['NH3'].median()))
# df1['CO']=df1['CO'].fillna((df1['CO'].median()))
# df1['SO2']=df1['SO2'].fillna((df1['SO2'].median()))
# df1['O3']=df1['O3'].fillna((df1['O3'].median()))
# df1['Benzene']=df1['Benzene'].fillna((df1['Benzene'].median()))
# df1['Toluene']=df1['Toluene'].fillna((df1['Toluene'].median()))
# df1['Xylene']=df1['Xylene'].fillna((df1['Xylene'].median()))
# df1['AQI']=df1['AQI'].fillna((df1['AQI'].median()))
# df1['AQI_Bucket']=df1['AQI_Bucket'].fillna('Moderate')
# arr = df1.to_numpy()
# list_arr = arr.tolist()
# for row in list_arr:
#     c = Pollution(City=row[0].upper(), Date=row[1], Pm2=row[2], Pm10=row[3], No=row[4], No2=row[5], Nox=row[6], 
#     Nh3=row[7], Co=row[8], So2=row[9], O3=row[10], Benzene=row[11], Toluene=row[12], Xylene=row[13], Aqi=row[14], Air_quality=row[15])
#     c.save()