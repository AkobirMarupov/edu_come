from django.urls import path
from admin_page.api_endpoints.views import (
    NotificationListAPIView, HeroBannerDetailAPIView,
    NotificationMarkReadAPIView, HeroBannerAPIView,
    HeroBannerCreateAPIView
)

urlpatterns = [
    path('hero-banner/', HeroBannerAPIView.as_view(), name='hero-banner'),
    path('banners/create/', HeroBannerCreateAPIView.as_view(), name='banner-create'),
    path('banners/<int:pk>/', HeroBannerDetailAPIView.as_view(), name='banner-detail'),

    path('notifications/', NotificationListAPIView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/mark-as-read/', NotificationMarkReadAPIView.as_view(), name='notification-read'),
]