from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings
from home.views import add_profile

urlpatterns = [
    path('', views.index),
    path('tintuc', views.index1),
    path('khoahoc', views.index2),
    path('info/', views.infomation),
    path('contact/', views.contact),
    path('register/', views.register, name="register"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_profile/', views.add_profile, name='add_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
