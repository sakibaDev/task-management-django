from django.urls import path
from tasks.views import home 

urlpatterns = [
    path('home/',home)
]