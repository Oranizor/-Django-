"""bysms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from sales.views import listorders, listcustomers
from mgr.customer import dispatcher
from mgr.sigininout import LoginView,signout,UserView
from mgr import UserView as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('guifan/shabi/sales/',listorders),
    path('allcustomers/',listcustomers),
    path('userlist/',views.UserView.as_view()),
    path('user/',UserView.as_view),
    path('dispatcher/',dispatcher),
    path('adminsignin/',LoginView.as_view()),
    path('adminsignout/',signout)
]
