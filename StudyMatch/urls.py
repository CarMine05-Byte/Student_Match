"""
URL configuration for study match project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from studymatch import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.registration, name='registration'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('gruppi/', views.gruppi, name='gruppi'),
    path('dettaglio_gruppo', views.dettaglio_gruppo, name='dettaglio_gruppo'),
    path('crea_gruppo', views.crea_gruppo, name='crea_gruppo'),
    path('esami', views.esame, name='esami'),
    path('notifiche/', views.notifica, name='notifiche'),
path('logout/', views.logout, name='logout')

]
