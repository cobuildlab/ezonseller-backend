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
from django.urls import path, re_path, include
from account import views as account_views
from product import views as product_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'accounts/profile', account_views.ProfileViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', account_views.Login.as_view()),
    path('logout/', account_views.Logout.as_view()),
    path('accounts/register/', account_views.RegisterView.as_view()),
    path('accounts/recoverypassword/', account_views.RequestRecoverPassword.as_view()),
    path('accounts/changepassword/', account_views.RecoverPasswordView.as_view()),
    path('accounts/profilechangepassword/', account_views.ChangePasswordView.as_view()),
    path('', include(router.urls)),
    re_path(r'^activate/$',account_views.ActivateAccountView.as_view()),
    path('amazon/', product_views.SearchAmazonView.as_view()),
    path('ebay/', product_views.SearchEbayView.as_view()),
]
from django.conf.urls.static import static, serve
from ezonseller import settings

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    ]