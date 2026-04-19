from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from course.api_endpoints.lesson.serializers import CourseSerializer, LessonSerializer
from course.models import Course, Lesson


class CourseListAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(responses={200: CourseSerializer(many=True)}, tags=['course'])
    def get(self, request):
        courses = Course.objects.all().order_by('-id')
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseSerializer, tags=['course'])
    def post(self, request):
        """Kurs yaratish (Faqat login qilganlar uchun)"""
        serializer = CourseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user) # Kurs egasini biriktirish
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class CourseDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(responses={200: CourseSerializer()}, tags=['course'])
    def get(self, request, pk):
        course = get_object_or_404(Course, owner=request.user, pk=pk)
        serializer = CourseSerializer(course, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseSerializer, tags=['course'])
    def put(self, request, pk):
        course = get_object_or_404(Course, owner=request.user, pk=pk)
        serializer = CourseSerializer(course, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    @swagger_auto_schema(tags=['course'])
    def delete(self, request, pk):
        course = get_object_or_404(Course, owner=request.user, pk=pk)
        course.delete()
        return Response({"message": "Kurs o'chirildi"}, status=status.HTTP_204_NO_CONTENT)


class LessonListAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(responses={200: LessonSerializer(many=True)}, tags=['lesson'])
    def get(self, request):
        lessons = Lesson.objects.all().order_by('-id')
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=LessonSerializer, tags=['lesson'])
    def post(self, request):
        serializer = LessonSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LessonDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(responses={200: LessonSerializer()}, tags=['lesson'])
    def get(self, request, pk):
        lesson = get_object_or_404(Lesson, course__owner=request.user, pk=pk)
        serializer = LessonSerializer(lesson, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=LessonSerializer, tags=['lesson'])
    def put(self, request, pk):
        lesson = get_object_or_404(Lesson, course__owner=request.user, pk=pk)
        serializer = LessonSerializer(lesson, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    @swagger_auto_schema(tags=['lesson'])
    def delete(self, request, pk):
        lesson = get_object_or_404(Lesson, course__owner=request.user, pk=pk)
        lesson.delete()
        return Response({"message": "Dars o'chirildi"})