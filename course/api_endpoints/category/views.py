from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.permissions import IsAdminUserRole
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from course.api_endpoints.category.serializers import CategorySerializer, SubCategorySerializer
from course.models import Category, SubCategory



class CategoryListAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['category'], operation_summary="Barcha kategoriyalar ro'yxati")
    def get(self, request):
        categories = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class MyCategoryAPIView(APIView):
    permission_classes = [IsAdminUserRole]
    
    @swagger_auto_schema(tags=['category'], operation_summary="Adminning o'zi yaratgan kategoriyalar")
    def get(self, request):
        categories = Category.objects.filter(course__owner=request.user).distinct().order_by('-id')
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer, tags=['category'])
    def post(self, request):
        serializer = CategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoryDetailAPIView(APIView):
    permission_classes = [IsAdminUserRole]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(responses={200: CategorySerializer()}, tags=['category'])
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer, tags=['category'])
    def put(self, request, pk):
        category = get_object_or_404(Category, course__owner=request.user, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    @swagger_auto_schema(tags=['category'])
    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response({"message": "Ma'lumot o'chirildi"})
    

class SubCategoryListAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['subcategory'], operation_summary="Barcha subkategoriyalar ro'yxati (Public)")
    def get(self, request):
        subcategories = SubCategory.objects.all().order_by('-id')
        serializer = SubCategorySerializer(subcategories, many=True, context={'request': request})
        return Response(serializer.data)


class MySubCategoryListAPIView(APIView):
    permission_classes = [IsAdminUserRole]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(tags=['subcategory'], operation_summary="Adminning o'z subkategoriyalari")
    def get(self, request):
        subcategories = SubCategory.objects.filter(category__course__owner=request.user).order_by('-id')
        serializer = SubCategorySerializer(subcategories, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=SubCategorySerializer, tags=['subcategory'])
    def post(self, request):
        serializer = SubCategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class SubCategoryDetailAPIView(APIView):
    permission_classes = [IsAdminUserRole]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(responses={200: SubCategorySerializer()}, tags=['subcategory'])
    def get(self, request, pk):
        subcategory = get_object_or_404(SubCategory, pk=pk)
        serializer = SubCategorySerializer(subcategory, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=SubCategorySerializer, tags=['subcategory'])
    def put(self, request, pk):
        subcategory = get_object_or_404(SubCategory, pk=pk)
        serializer = SubCategorySerializer(subcategory, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    @swagger_auto_schema(tags=['subcategory'])
    def delete(self, request, pk):
        subcategory = get_object_or_404(SubCategory, pk=pk)
        subcategory.delete()
        return Response({"message": "Ma'lumot o'chirildi"})