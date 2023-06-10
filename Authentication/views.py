from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.
def home(request):
    return render(request,'Authentication/index.html')

def signup(request):

    if request.method=='POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exits! PLease try some other username.")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,"Email already exits")
            return redirect('home')
        if len(username)>10:
            messages.error(request,"Username should be less than 10 character")
        if pass1 != pass2:
            messages.error(request,"Password didn't match")

        if not username.isalnum():
            messages.error(request,"Username must be alpha-Numeric ")
            return redirect('home')


        myuser= User.objects.create_user(username,email,pass1)
        myuser.first_name =fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request,"Your account has been successfully created .")

        #Welcome email

        subject = "welcome to Joshua Login System"
        message = "Hello" + myuser.first_name + "!! \n"+"Welcome to My LoginSystem !! \n Thankyou for visiting our website "
        from_email= settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        return redirect('signin')


    return render(request,'Authentication/signup.html')

def signin(request):

    if request.method=='POST':
        username=request.POST['username']
        pass1=request.POST['pass1']

        user=authenticate(username=username,password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,'Authentication/index.html',{'fname': fname })

        else:
            messages.error(request,"Bad Credentials! ")
            return redirect('home')


    return render(request,'Authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request,"Logged Out Succesfully")
    return redirect('home')