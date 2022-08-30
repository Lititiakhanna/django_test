from .views import RegisterAPI, LoginAPI, LoginOperationalAPI, LoginClientAPI
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/loginOperational/', LoginOperationalAPI.as_view(), name='login_operational'),
    path('api/loginClient/', LoginClientAPI.as_view(), name='login_client'),
]