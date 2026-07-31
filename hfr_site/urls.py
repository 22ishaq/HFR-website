from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('index.html', views.home),
    path('about/', views.page, {'template_name': 'core/about.html'}, name='about'),
    path('divisions/', views.page, {'template_name': 'core/divisions.html'}, name='divisions'),
    path('competitions/', views.page, {'template_name': 'core/competitions.html'}, name='competitions'),
    path('events/', views.page, {'template_name': 'core/events.html'}, name='events'),
    path('register/', views.page, {'template_name': 'core/register.html'}, name='register'),
    path('register.html', views.page, {'template_name': 'core/register.html'}),
    path('shop/', views.page, {'template_name': 'core/shop.html'}, name='shop'),
    path('sponsors/', views.page, {'template_name': 'core/sponsors.html'}, name='sponsors'),
]
