from django.urls import path
from .import views

urlpatterns = [
    path("",views.Index,name="Index"),
    path("MerchantIndex",views.MerchantIndex,name="MerchantIndex"),
    path("AdminIndex",views.AdminIndex,name="AdminIndex"),

    path('SignIn',views.SignIn,name="SignIn"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignOut",views.SignOut,name="SignOut"),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate, name='activate'),

]