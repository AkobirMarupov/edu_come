from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .serializers import (
        SellerCreateSerializer,
        VerifyOTPSerializer,
        SetNewPasswordSerializer,
        LoginSerializer,
        )
from django.contrib.auth.hashers import make_password

from account.models import User
from .serializers import CheckPhoneSerializer
from account.utils import send_eskiz_sms


class LoginAPIView(APIView):
    #LOgin qilganda hammaga ruxsat berilishi kerak, shuning uchun AllowAny ni ishlatamiz
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    # post yaratishimiz uchun funksiya yaratamiz va login qilamiz 
    def post(self, request):
        # telefon raqamni olish uchun request.data dan phone_number ni olamiz, sababi telefon raqamni tekshirish uchun ishlatamiz
        phone_number = request.data.get('phone_number')
        # parolni olish uchun request.data dan password ni olamiz
        password = request.data.get('password')

        # user ni olamiz va u userdagi pfone_number bazada bolsa filter qilib olamiz, agar topilmasa first() bilan None qaytaradi
        user = User.objects.filter(phone_number=phone_number).first()

        #agar user topilsa va parol tekshirilsa, lekin user faollashtirilmagan bolsa xato qaytaradi,  check_password() metodi parolni tekshiradi va agar to'g'ri bo'lsa True qaytaradi, aks holda False qaytaradi
        if user and user.check_password(password):
            #agar user faollashtirilmagan bolsa xato qaytaradi, is_active atributi user modelida mavjud bo'lishi kerak, bu atribut userning faollashtirilgan yoki faollashtirilmaganligini ko'rsatadi
            if not user.is_active:
                return Response({"detail": "Hisobingiz faollashtirilmagan. Iltimos, administrator bilan bog'laning."}, status=status.HTTP_403_FORBIDDEN)

            # refresh token yaratish uchun RefreshToken.for_user() metodidan foydalanamiz, bu metod user ni qabul qiladi va refresh tokenni yaratadi
            refresh = RefreshToken.for_user(user)
            # access tokenni olish uchun refresh tokenning access atributidan foydalanamiz, bu access tokenni yaratadi
            access_token = str(refresh.access_token)
            # refresh tokenni olish uchun refresh tokenni stringga aylantiramiz, bu refresh tokenni yaratadi
            refresh_token = str(refresh)

            # response orqali accsess tokenni qaytarazmiz va vazifasi tokenni bizga kerak bo'lgan joylarda ishlatish uchun, masalan, protected endpointlarga kirishda tokenni tekshirish uchun ishlatamiz
            response = Response({'accsess': access_token}, status=status.HTTP_200_OK)

            # refresh tokenni cookiega saqlaymiz, bu refresh tokenni keyinchalik ishlatish uchun, masalan, access tokenni yangilashda refresh tokenni tekshirish uchun ishlatamiz
            response.set_cookie(
                key='refresh_token',  # cookie nomi
                value=refresh_token,  # cookie qiymati, bu refresh tokenni o'z ichiga oladi
                httponly=True,  # JavaScript orqali cookiega kirishni oldini oladi, bu xavfsizlikni oshiradi
                secure=True,  # faqat HTTPS orqali cookie yuborilishini ta'minlaydi, bu xavfsizlikni oshiradi
                samesite='Lax',  # cookieni cross-site so'rovlarida yuborilishini boshqaradi, bu yerda 'Lax' deb belgilangan, bu cookieni faqat birinchi tomon so'rovlarida yuborilishini ta'minlaydi
                max_age=7 * 24 * 60 * 60,  # cookie amal qilish muddati, bu yerda 7 kun (7 kun * 24 soat * 60 daqiqa * 60 sekund)
            )

            return response
        
        # buyerda aagar user topilmasa yoki parol noto'g'ri bo'lsa, xato javob qaytaradi, bu yerda 401 Unauthorized status kodi ishlatiladi, bu foydalanuvchi autentifikatsiya qilinmaganligini bildiradi
        return Response({"detail": "Telefon raqam yoki parol xato. Qaytadan urinib ko'ring."}, status=status.HTTP_401_UNAUTHORIZED) 
    