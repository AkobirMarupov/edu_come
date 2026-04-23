from rest_framework import serializers
from course.models import Enrollment, Course

class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source='course.title')
    course_image = serializers.ImageField(source='course.image', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'course_title', 'course_image']

    def validate(self, attrs):
        user = attrs.get('user')
        course = attrs.get('course')

        if Enrollment.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("Siz allaqachon ushbu kursga a'zo bo'lgansiz!")
        
        return attrs