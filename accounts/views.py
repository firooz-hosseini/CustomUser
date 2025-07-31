from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import CustomUser
from django.views.generic import View,DetailView
from .forms import MyUserCreationForm, ConfirmForm, LoginForm,ResetPasswordForm,MobileForm
import random
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser

class SignUpView(View):

    html_file = 'signup.html'
    form = MyUserCreationForm()

    def get(self, request):
        return render(request, self.html_file, {'form': self.form})
    
    def post(self, request):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data.get('mobile')
            user = CustomUser.objects.filter(mobile = mobile).exists()
            if not user :
                code = str(random.randint(1000,9999))
                request.session['user_registration_info'] = {
                                'mobile': form.cleaned_data['mobile'],
                                'password': form.cleaned_data['password'],
                                'code':code,
                        }
                print('confirmation code:', code)
                return redirect('confirm')


class ConfirmSignUpView(View):

    def get(self, request):
        form = ConfirmForm()
        return render(request, 'confirm.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        form = ConfirmForm(request.POST)
        if form.is_valid():
            verified_code = form.cleaned_data['confirm_code']
            if verified_code == user_session.get('code'):
                mobile = user_session.get('mobile')
                password = user_session.get('password')
                CustomUser.objects.create_user(mobile = mobile, password=password) # type: ignore
                del request.session['user_registration_info']
                return redirect('login')           
            else:
                return HttpResponse('error')
            

class LoginView(View):
    
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data.get('mobile')
            password = form.cleaned_data.get('password')
            user = authenticate(mobile=mobile, password=password)
            if user:
                login(request, user)
                return redirect('profile')      
               

class Profile(DetailView):

    model = CustomUser
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user 


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login')
    

def home(request):
    return render(request,'home.html')

def mobile(request):

    if request.method == "POST":
        form = MobileForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            code = str(random.randint(1000,9999))
            request.session['CodeCheck'] = {'code':code,'mobile':mobile}
            print('confirmation code:', code)
            return redirect('confirmresetpassword')
        
    form = MobileForm()
    return render(request,'mobile.html',{'form':form})

class ConfirmResetPasswordView(View):

    def get(self, request):
        form = ConfirmForm()
        return render(request, 'confirm.html', {'form': form})

    def post(self, request):
        previous_code = request.session['CodeCheck']['code']
        form = ConfirmForm(request.POST)
        if form.is_valid():
            verified_code = form.cleaned_data['confirm_code']
            if verified_code == previous_code:
                return redirect('resetpassword')           
            else:
                return HttpResponse('error')      
    
def ResetPassword(request):

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pass1 = data['password1']
            pass2 = data['password2']
            if pass1 == pass2:
                mobile = request.session['CodeCheck']['mobile']
                user = CustomUser.objects.get(mobile = mobile)
                user.set_password(pass1)
                user.save()
                del request.session['CodeCheck']
                return redirect('login')
            
    form = ResetPasswordForm()
    return render(request,'resetpassword.html',{'form':form})