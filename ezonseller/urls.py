"""ezonseller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from account import views as account_views
#from rest_framework import routers

#router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', account_views.Login.as_view()),
    path('logout/', account_views.Logout.as_view()),
    path('accounts/register/', account_views.RegisterView.as_view()),
    path('accounts/recoverypassword/', account_views.RequestRecoverPassword.as_view()),
    path('accounts/changepassword/', account_views.RecoverPasswordView.as_view()),
    path('accounts/profilechangepassword/', account_views.ChangePasswordView.as_view()),
    path('example', account_views.example.as_view()),
    #path('recibir/', account_views.recibir.as_view()),
    #re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',account_views.activate.as_view()),
    #re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/$',account_views.activate.as_view()),
    #path('activate/<str:uidb64>/<str:token>/',account_views.activate.as_view()),
    re_path(r'^activate/$',account_views.activate.as_view()),
]
