from django.shortcuts import render
from email.message import EmailMessage
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from gfg import  settings






from django.core.mail import send_mail,EmailMessage






# Create your views here.
def home(request):
    return render(request,"authentication/index.html")
def signup(request):
    
    if request.method =="POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exist")
            return redirect('home')

        if User.objects.filter(email=email):

            messages.error(request,"email already exist")
            return redirect('home')
        if len(username)>10:
            messages.error(request,"Username must be less than 10 characters")
        if pass1 != pass2:
            messages.error('Password did not match')
        if not username.isalnum():
            messages.error('username must be alpha-numric!')
            return redirect('home')
        myuser= User.objects.create_user(username,email,pass1)
        myuser.first_name =fname
        myuser.lastname =lname
        
    

        
    

        myuser.save()
        


        messages.success(request,"Your account is created, pleaase confirm your  email to proceed through email verification page" )
        # welcome email
        subject ="Welcome to poll"
        message = "Hello" + myuser.first_name +"!! \n" +  "Welcome to poll ."
        from_email= settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject ,message,from_email,to_list,fail_silently=True)   

        
       
       
       
        return redirect("signin")


    
    
    
    return render(request,"authentication/signup.html")
def signin(request):
    


    if request.method =="POST":

        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username= username, password= pass1)
        if user is not None:



            login(request,user)
            fname = user.first_name
            return render(request,"authentication/index.html",{'fname':fname})


        else:

            messages.error(request,"Bad credentials")
            return redirect('home')
   
   
   
   
   
    return render(request,"authentication/signin.html")
def signout(request):
    logout(request)
    messages.success(request,"logged out succesfullly")
    return redirect('home')

def profile(request):
    
    contex={
        'user':request.user

    }
    return render(request,"authentication/profile.html")
def celery(request):
    return HttpResponse("heloo")
# Create your views here.
