from django.urls import path 
from .import views
urlpatterns = [
    path("",views.index,name="Home"),
    path('sign_up',views.sign_up,name='Sign_up'),
    path('sign_up_logic',views.sign_up_logic,name='spl'),
]
