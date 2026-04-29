from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from account.permissions import IsAdminUserRole
from admin_page.models import Notification, HeroBanner
from admin_page.api_endpoints.serializers import NotificationSerializer, HeroBannerSerializer


class NotificationListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(responses={200: NotificationSerializer(many=True)}, tags=['notification'])
    def get(self, request):
        notification = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notification, many=True)
        return Response(serializer.data)
    


class NotificationMarkReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['notification'], operation_description="Xabarni oqildi deb belgilaymiz.")
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({'message': 'Xabar oqildi.'}, status=status.HTTP_200_OK)
    


class HeroBannerAPIView(APIView):
    permission_classes = []

    @swagger_auto_schema(responses={200: HeroBannerSerializer()}, tags=['banner'])
    def get(self, request):
        banner = HeroBanner.objects.filter(is_active=True).last()
        if not banner:
            return Response({'message': 'Aktiv banner topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = HeroBannerSerializer(banner)
        return Response(serializer.data)
    


class HeroBannerCreateAPIView(APIView):
    permission_classes = [IsAdminUserRole]

    @swagger_auto_schema(request_body=HeroBannerSerializer, tags=['banner'])
    def post(self, request):
        serializer = HeroBannerSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):

            if serializer.validated_data.get('is_active', False):
                HeroBanner.objects.filter(is_active=True).update(is_active=False)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    

class HeroBannerDetailAPIView(APIView):
    permission_classes = [IsAdminUserRole]
    

    @swagger_auto_schema(responses={200: HeroBannerSerializer}, tags=['banner'])
    def get(self, request, pk):
        banner = HeroBanner.objects.filter(pk=pk).first()

        if not banner:
            return Response({"meesage": "Malumotlar topilmadi."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = HeroBannerSerializer(banner, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def put(self, request, pk):
        try:
            banner = HeroBanner.objects.get(pk=pk)
        except HeroBanner.DoesNotExist:
            return Response({"message": "Bu id da banner yo‘q"},status=404)

        serializer = HeroBannerSerializer(banner, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data.get('is_active', False):
                HeroBanner.objects.filter(is_active=True).exclude(pk=pk).update(is_active=False)

            serializer.save()

        return Response(serializer.data)
            