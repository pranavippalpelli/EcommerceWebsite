from django.urls import path
from ecommerceapp import views

urlpatterns = [
    path('',views.index),
    path('contact',views.contact),
    path('about',views.about),
    path('signin',views.signin),
    path('checkout',views.checkout),
    path('tracker',views.tracker),
    path('demoo',views.demoo),
    path('media/<int:id>',views.productview),   #getting product by using  id 

]
