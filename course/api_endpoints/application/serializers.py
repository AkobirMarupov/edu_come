from rest_framework import serializers
from course.models import CourseApplication, Enrollment, Review, Wishlist
from account.models import User 


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'avatar', 'phone_number']


class CourseApplicationSerializer(serializers.ModelSerializer):
    user_details = UserMinimalSerializer(source='user', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = CourseApplication
        fields = [
            'id', 'user_details', 'course', 'course_title', 
            'status', 'status_display', 'message', 'created_at'
        ]
        read_only_fields = ['status']

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("Foydalanuvchi aniqlanmadi.")

        user = request.user
        course = attrs.get('course')
        
        if course.owner == user:
            raise serializers.ValidationError({
                "course": "Siz o'qituvchisiz, kurslarni sotib ololmaysiz."
            })
        if CourseApplication.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError({
                "course": "Siz allaqachon ushbu kursga ariza yuborgansiz."
            })
            
        return attrs

