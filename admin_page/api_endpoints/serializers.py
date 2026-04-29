from rest_framework import serializers

from admin_page.models import Notification, HeroBanner


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'body', 'is_read']
        read_only_fields = ['user', 'created_at']



class HeroBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroBanner
        fields = [
            'id', 'title', 'subtitle', 
            'courses_count_text', 'students_count_text', 'rating_text', 
            'background_gradient', 'image'
        ]
