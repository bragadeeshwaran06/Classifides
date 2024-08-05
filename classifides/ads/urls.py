from django.urls import path
from ads.views import *
from ads import views
urlpatterns = [
    path('',views.home,name='home'),
    path('category/<int:category_id>/', category_ads, name='category_ads'),
]

