from django.urls import path
from home import views

urlpatterns = [
    path('',views.Login, name='home'),
    path('home/',views.chat, name='home'),
 
]