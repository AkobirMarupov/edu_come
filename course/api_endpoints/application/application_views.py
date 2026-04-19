from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from course.models import CourseApplication, Enrollment
from .serializers import CourseApplicationSerializer


class CourseApplicationListAPIView(APIView):
    permission_classes = []
    
    @swagger_auto_schema(responses={200: CourseApplicationSerializer(many=True)}, tags=['application'])
    def get(self, request):
        if request.user.role == 'teacher':
            applications = CourseApplication.objects.filter(course__owner=request.user)
        else:
            applications = CourseApplication.objects.filter(user=request.user)
        serializer = CourseApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CourseApplicationSerializer, 
        operation_description="Kursga ariza yuborish. User avtomatik request.user dan olinadi.",
        tags=['application']
    )
    def post(self, request):
        serializer = CourseApplicationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class CourseApplicationApproveAPIView(APIView):
    permission_classes = []

    @swagger_auto_schema(tags=['application'], operation_description="Arizani tasdiqlash (Faqat o'qituvchi)")
    def post(self, request, pk):
        application = get_object_or_404(CourseApplication, pk=pk, course__owner=request.user)
        application.status = 'approved'
        application.save()
        Enrollment.objects.get_or_create(user=application.user, course=application.course)
        return Response({"message": "Ariza tasdiqlandi va talaba kursga qo'shildi"})
    
    @swagger_auto_schema(request_body=CourseApplicationSerializer, tags=['application'])
    def put(self, request, pk):
        appl = get_object_or_404(CourseApplication, course__owner=request.user, pk=pk)
        serializer = CourseApplicationSerializer(appl, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    @swagger_auto_schema(tags=['application'])
    def delete(self, request, pk):
        appl = CourseApplication.objects.get(pk=pk)
        appl.delete()
        return Response({"message": "Comment o'chirildi"})
