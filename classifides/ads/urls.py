from django.urls import path
from ads.views import *
from ads import views

urlpatterns = [
    path('',views.home,name='home'),
    path('category/<int:category_id>/', category_ads, name='category_ads'),
    path('post_ad/', post_ad, name='post_ad'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('ad/<int:ad_id>/like/', views.like_ad, name='like_ad'),
    path('ads/my_ads/', MyAdsView.as_view(), name='my_ads'),
    path('ads/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('ads/delete/<int:pk>/', delete_ad, name='delete_ad'),
    path('delete/', delete_image, name='delete_image'),
]

