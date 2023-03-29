from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm,UserChangeForm
from django.http import HttpResponseRedirect
from .forms import SignUpForm,EditUserForm
from django.contrib import messages
from django.urls import reverse
# Create your views here.


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm=SignUpForm(request.POST)
            # print(fm)
            if fm.is_valid():
                messages.success(request,'Account created successfully!!!')
                fm.save()
        else:
            fm=SignUpForm()
        return render(request,'Applogin/signup.html',{'forms':fm})
    else:
        print("2")
        return HttpResponseRedirect(reverse("starting-page"))


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
                fm=AuthenticationForm(request=request,data=request.POST)
                print(request.POST)
                if fm.is_valid():
                    print("1")
                    uname=fm.cleaned_data['username']
                    upass=fm.cleaned_data['password']
                    user=authenticate(username=uname,password=upass)
                    print(user)
                    if user is not None:
                        login(request,user)
                        request.session['name']=uname
                        return HttpResponseRedirect(reverse('starting-page'))
                
        else:
            fm=AuthenticationForm()
        return render(request,'Applogin/login.html',{'forms':fm})
    
    else:
        print("2")
        return HttpResponseRedirect(reverse("starting-page"))

def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm=EditUserForm(request.POST,instance=request.user)
            if fm.is_valid():
                messages.success(request,'Profile change successfully!!!')
                fm.save()
        else:
            fm=EditUserForm(instance=request.user)
        return render(request,'Applogin/user_profile.html',{'name':request.user,'form':fm})
    else:
        return HttpResponseRedirect('/login')

def user_logout(request):
    logout(request)
    return redirect(reverse('starting-page'))