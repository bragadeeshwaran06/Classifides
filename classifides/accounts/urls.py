from django.urls import path,include
from .views import *
from .views import user_profile

urlpatterns = [
    path('register/',register,name='register'),
    path('profile/', user_profile, name='user_profile'),
    path('',include('django.contrib.auth.urls')),
]
