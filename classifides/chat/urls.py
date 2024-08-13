from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:ad_id>/<int:user_id>/', views.conversation, name='conversation'),
]
