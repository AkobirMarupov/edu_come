from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from course.api_endpoints.review.serializer import EnrollmentSerializer
from course.models import Enrollment, Review, Wishlist


class EnrollmentAPIVIew(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(responses={200: EnrollmentSerializer(many=True)}, tags=['enrollments'])
    def get(self, request):
        enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    

    @swagger_auto_schema(request_body=EnrollmentSerializer, tags=['enrollments'])
    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EnrollmentDetailAPIVIew(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk):
        try:
            enrollment = Enrollment.objects.get(pk=pk, user=request.user)
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data)
        except Enrollment.DoesNotExist:
            return Response({'message': 'Bunday azolik malumoti topilmadi'}, 
            status=status.HTTP_404_NOT_FOUND
            )


    @swagger_auto_schema(request_body=EnrollmentSerializer, tags=['enrollments'])
    def put(self, request, pk):
        try:
            enrollment = Enrollment.objects.get(pk=pk, user=request.user)
            serializer = EnrollmentSerializer(enrollment, data=request.data, context={'request': request}, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Enrollment.DoesNotExist:
            return Response({"message": "Yangilash uchun bunday a'zolik mavjud emas"}, 
                status=status.HTTP_404_NOT_FOUND)


    @swagger_auto_schema(tags=['enrollments'])
    def delete(self, request, pk):
        try:
            enrollment = Enrollment.objects.get(pk=pk, user=request.user)
            enrollment.delete()
            return Response(
                {"message": "Azolik muvaffaqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT )
        except Enrollment.DoesNotExist:
            return Response(
                {'message': 'Bunday azolik ma\'lumoti topilmadi'}, status=status.HTTP_404_NOT_FOUND)