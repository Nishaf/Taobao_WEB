"""Taobao_WEB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^results/', Search_Results.as_view(), name="results"),
    url(r'^search/', Search_Results.as_view(), name="search"),
    url(r'^signup/', SignUp.as_view(), name="signup"),
    url(r'^profile_view/', Profile.as_view(), name="profile"),
    url(r'^edit_info/', EditInfo.as_view(), name="edit_info"),
    url(r'^logout/', Logout.as_view(), name="logout"),
    url(r'^login/', Login.as_view(), name="login"),
    url(r'^search_item/', Search_Items.as_view(), name="Search_Items"),
    url(r'^', ABC.as_view(), name="index"),
]
