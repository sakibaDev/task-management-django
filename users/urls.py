from django.urls import path
from users.views import sign_up,register_view,sign_in,signout
urlpatterns = [

    path('sign-up/',sign_up,name='sign-up'),
    path('register/', register_view, name='register'),
    path('sign-in/',sign_in,name='sign-in'),
    path('signout/',signout,name="logout")

]
