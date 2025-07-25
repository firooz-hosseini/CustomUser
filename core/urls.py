from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name= 'signup'),
    path('confirm/', views.ConfirmView.as_view(), name= 'confirm'),

]