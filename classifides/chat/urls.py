from django.urls import path
from chat.views import *

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    path('conversation/<int:ad_id>/<int:user_id>/', conversation, name='conversation'),
    path('edit-message/<int:message_id>/', edit_message, name='edit_message'),
    path('delete-message/<int:message_id>/', delete_message, name='delete_message'),
]
