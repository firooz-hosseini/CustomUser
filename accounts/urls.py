from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name= 'signup'),
    path('confirmsignup/', views.ConfirmSignUpView.as_view(), name= 'confirmsignup'),
    path('login/', views.LoginView.as_view(), name= 'login'),
    path('profile/', views.Profile.as_view(), name= 'profile'),
    path('logout/', views.LogoutView.as_view(), name= 'logout'),
    path('resetpassword/', views.ResetPassword, name= 'resetpassword'), # type: ignore
    path('mobile/', views.mobile, name= 'mobile'),
    path('confirmresetpassword/', views.ConfirmResetPasswordView.as_view(), name= 'confirmresetpassword'),
]