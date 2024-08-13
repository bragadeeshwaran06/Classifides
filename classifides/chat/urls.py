from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.message_list, name='message_list'),
    path('messages/send/<int:ad_id>/<int:receiver_id>/', views.send_message, name='send_message'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
]
