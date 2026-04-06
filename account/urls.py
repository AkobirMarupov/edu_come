from django.urls import path

from account.api_endpoints.auth.views import LoginAPIView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
]