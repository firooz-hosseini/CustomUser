from django.contrib import admin
from django.urls import path, include
from accounts.views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'), # type: ignore
    path('accounts/', include('accounts.urls')),
]
