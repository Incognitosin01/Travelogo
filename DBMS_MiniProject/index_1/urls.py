from django.urls import path 
from .import views
urlpatterns = [
    path("",views.index,name="Home"),
    path('sign_up',views.sign_up,name='Sign_up'),
    path('sign_up_logic',views.sign_up_logic,name='spl'),
    path('sign_in',views.sign_in,name='sign_in'),
    path('agencies',views.agencies_deal,name='agency_deal')
]
