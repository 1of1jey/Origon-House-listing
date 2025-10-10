from django.urls import path
from . import views

app_name = 'host_auth'

urlpatterns = [
    path('api/register/', views.HostRegisterAPIView.as_view(), name='api_host_register'),
    path('api/login/', views.HostLoginAPIView.as_view(), name='api_host_login'),
    path('api/logout/', views.HostLogoutAPIView.as_view(), name='api_host_logout'),
    path('api/profile/', views.HostProfileAPIView.as_view(), name='api_host_profile'),
    path('api/change-password/', views.ChangeHostPasswordAPIView.as_view(), name='api_host_change_password'),
    path('api/details/', views.host_detail_view, name='api_host_detail'),
    path('api/verification-status/', views.host_verification_status, name='api_host_verification'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('host/', include('host_auth.urls')),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
]

