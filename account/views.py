from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.sessions.models import Session

# Create your views here.


def signup(request):
    if request.method == "POST":
        postdata = request.POST
        firstname = postdata.get('firstname')
        lastname = postdata.get('lastname')
        email = postdata.get('email')
        gender = postdata.get('gender')
        city = postdata.get('city')
        password = postdata.get('password')
        confirm_password = postdata.get('confirm_password')
        username = postdata.get('username')
        if gender == 'option1':
            gender = 'M'
        else:
            gender = 'F'
        
        user = User.objects.create(username=username,email=email,password=password)
        #user.set_password(password)
        user.save()
        messages.success(request,"You have been successfully registered")
        return redirect('login')
    else:
        return render(request,'account/register.html')
        

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        print(user,username,password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are now logged in")
            return redirect('index')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('login')
    return render(request,'account/login.html')


def logout(request):
    auth.logout(request)
    messages.success(request,"You've been logged out")
    return redirect('login')