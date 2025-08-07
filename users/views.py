from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from users.forms import CustomRegistrationForm
from django.contrib import messages


# Create your views here.

def sign_up(request):

    if request.method == 'GET':
        form=CustomRegistrationForm()

    if request.method=='POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

    
    
    return render(request,'registration/register.html',{'form':form})

def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your registration is completed!')
            return redirect('register')
        else:
            form = CustomRegistrationForm()

        return render(request,'register.html',{'form':form})


def sign_in(request):

    if request.method == 'POST':
      
      username = request.POST.get('username')
      password = request.POST.get('password')
      
      user = authenticate(request,username=username,password=password)

      print(user)
      if user is not None:
          login(request,user)

          return redirect('home')

    return render(request,'registration/login.html')

from django.http import HttpResponseRedirect

def signout(request):
    if request.method in ['POST', 'GET']:
        logout(request)
        return redirect('sign-in')  # Or wherever you want to send the user
