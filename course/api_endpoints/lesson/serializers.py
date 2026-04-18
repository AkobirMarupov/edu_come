from rest_framework import serializers
from course.models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id', 
            'title',
            'description',
            'category',
            'sub_category',
            'price',
            'image_url',
            'owner'
        ]
        read_only_fields = ['id', 'owner']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'course',
            'title',
            'description',
            'video_url',
            'video_file',
            'duration_display'
        ]
        read_only_fields = ['id']