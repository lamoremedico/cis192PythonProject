"""NickJuliaOnlineJournal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('aboutus', views.splash, name="splash"),
    path('journalstats', views.journal_stats, name="journalstats"),
    path('favorite/<theEntry>/<typeofpage>/<whatpage>/', views.favorite, name='favorite'),
    path('pin/<theEntry>/<typeofpage>/<whatpage>/', views.pin, name='pin'),
    path('delete/<theEntry>/<typeofpage>/<whatpage>/', views.delete, name='delete'),
    path('login', views.login_, name="login"),
    path('signup', views.signup, name="login"),
    path('logout', views.logout_, name="logout"),
]