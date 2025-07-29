from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name= 'signup'),
    path('confirm/', views.ConfirmView.as_view(), name= 'confirm'),
    path('login/', views.LoginView.as_view(), name= 'login'),
    path('profile/', views.profile_view, name= 'profile'),
    path('logout/', views.LogoutView.as_view(), name= 'logout'),

]