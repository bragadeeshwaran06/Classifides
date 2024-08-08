from django.urls import path,include
from .views import *
from .views import user_profile
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('register/',register,name='register'),
    path('profile/', user_profile, name='user_profile'),
    
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),


    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),

    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
]
