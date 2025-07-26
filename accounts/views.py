from django.shortcuts import render, redirect
from .models import CustomUser
from django.views.generic import View
from .forms import MyUserCreationForm, ConfirmForm
import random
from django.http import HttpResponse


class SignUpView(View):

    html_file = 'signup_form.html'
    form = MyUserCreationForm()

    def get(self, request):
        return render(request, self.html_file, {'form': self.form})
    
    def post(self, request):
        filled_form = MyUserCreationForm(request.POST)
        if filled_form.is_valid():
            mobile = filled_form.cleaned_data.get('mobile')
            user = CustomUser.objects.filter(mobile = mobile).exists()
            if not user :
                code = random.randint(1000,9999)
                request.session['user_registration_info'] = {
                                'phone_number': filled_form.cleaned_data['mobile'],
                                'password': filled_form.cleaned_data['password'],
                                'code':code,
                        }
                print(code,'confirmation')
                return redirect('confirm')


class ConfirmView(View):

    def get(self, request):
        form = ConfirmForm()
        return render(request, 'confirm.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        filled_form = ConfirmForm(request.POST)
        if filled_form.is_valid():
            verified_code = filled_form.cleaned_data['confirm_code']
            if verified_code is user_session.get('code'):
                mobile = user_session.get('mobile')
                password = user_session.get('password')
                CustomUser.objects.create_user(mobile = mobile, password=password)
                del request.session['user_registration_info']
                return redirect('signup')
            
            else:
                return HttpResponse('error')