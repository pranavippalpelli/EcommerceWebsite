from django.urls import path
from authcart import views
 
urlpatterns = [
    path('signup/',views.signup),
    path('login/',views.handlelogin),
    path('logout/',views.handlelogout),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),

]
