from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recruitment.urls')),
    path('', views.home, name='home'),
    path('index.html', views.home),
    path('about/', views.page, {'template_name': 'core/about.html'}, name='about'),
    path('history/', views.page, {'template_name': 'core/history.html'}, name='history'),
    path('divisions/', views.page, {'template_name': 'core/divisions.html'}, name='divisions'),
    path('divisions/land/', views.page, {'template_name': 'core/division_land.html'}, name='division_land'),
    path('divisions/sea/', views.page, {'template_name': 'core/division_sea.html'}, name='division_sea'),
    path('divisions/air/', views.page, {'template_name': 'core/division_air.html'}, name='division_air'),
    path('divisions/operations/', views.page, {'template_name': 'core/division_ops.html'}, name='division_ops'),
    path('projects/aero-concept/', views.page, {'template_name': 'core/project_aero.html'}, name='project_aero'),
    path('projects/hydrogen-endurance-vehicle/', views.page, {'template_name': 'core/project_hev.html'}, name='project_hev'),
    path('projects/energy-class-boat/', views.page, {'template_name': 'core/project_boat.html'}, name='project_boat'),
    path('competitions/', views.page, {'template_name': 'core/competitions.html'}, name='competitions'),
    path('events/', views.page, {'template_name': 'core/events.html'}, name='events'),
    path('register/', views.page, {'template_name': 'core/register.html'}, name='register'),
    path('register.html', views.page, {'template_name': 'core/register.html'}),
    path('shop/', views.page, {'template_name': 'core/shop.html'}, name='shop'),
    path('sponsors/', views.page, {'template_name': 'core/sponsors.html'}, name='sponsors'),
    path('support-us/', views.page, {'template_name': 'core/support.html'}, name='support_us'),
]

# Uploaded avatars are served in production too. Traffic is small enough
# that Django serving them is fine; CVs are NOT here (see application_cv).
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
