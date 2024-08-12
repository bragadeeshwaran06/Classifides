from django.urls import path
from . import views


urlpatterns = [
    path('ad/<int:ad_id>/chat/', views.ad_chat, name='ad_chat'),
]