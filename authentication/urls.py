from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='api_logout'),
    path('api/profile/', views.UserProfileAPIView.as_view(), name='api_profile'),
    path('api/change-password/', views.ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('api/user/', views.user_detail_view, name='api_user_detail'),
]