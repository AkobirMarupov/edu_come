from django.urls import path

from account.api_endpoints.auth.views import (
    LoginAPIView, SendSMSAPIView, AdminCreateLoginAPIView, AdminListAPIView, 
    NewPassworAPIView, CreatePasswordAPIView, RefreshTokenAPIView,)


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('send-sms/', SendSMSAPIView.as_view(), name='send_sms'),
    path('admin/create-login/', AdminCreateLoginAPIView.as_view(), name='admin_create_login'),
    path('list/<int:pk>/', AdminListAPIView.as_view(), name='admin_list'),
    path('password/new/', NewPassworAPIView.as_view(), name='new_password'),
    path('password/create/', CreatePasswordAPIView.as_view(), name='create_password'),
    path('token/refresh/', RefreshTokenAPIView.as_view(), name='token_refresh'),
]