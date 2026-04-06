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

# LoginAPIView maqsadi foydalanuvchining telefon raqam va parol orqali login qilish, bu yerda telefon raqam va parol orqali login qilish uchun ishlatiladi
class LoginAPIView(APIView):
    #LOgin qilganda hammaga ruxsat berilishi kerak, shuning uchun AllowAny ni ishlatamiz
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer, tags=['Auth'])
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
    

# SendSMSAPIView maqsadi telefon raqamga sms yuborish, bu yerda telefon raqamga sms yuborish uchun ishlatiladi
class SendSMSAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=CheckPhoneSerializer, tags=['Auth'])
    def post(self, request):
        # serializerdan telefon raqamni olish uchun serializerni yaratamiz va request.data ni unga beramiz, bu serializer telefon raqamni tekshirish uchun ishlatiladi
        serializer = CheckPhoneSerializer(data=request.data)
        # agar serializer valid bo'lsa, ya'ni telefon raqam to'g'ri formatda bo'lsa va 
        # boshqa tekshiruvlardan o'tsa, sms yuborish funksiyasini chaqiramiz, bu funksiya telefon raqamga sms yuboradi va tasdiqlash kodini qaytaradi
        serializer.is_valid(raise_exception=True)

        # telefon raqamni serializer.validated_data dan olamiz, bu telefon raqamni tekshirish uchun ishlatiladi
        phone_number = serializer.validated_data['phone_number']
        # user ni filter qilib olamiz, agar user topilmasa None qaytaradi, bu userni tekshirish uchun ishlatiladi
        user = User.objects.filter(phone_number=phone_number).first()

        # agar user topilmasa, sms yuborish funksiyasini chaqiramiz, bu funksiya telefon raqamga sms yuboradi va tasdiqlash kodini qaytaradi, agar sms yuborish
        #  muvaffaqiyatli bo'lsa, tasdiqlash kodini user modelida saqlaymiz, bu tasdiqlash kodini keyinchalik tekshirish uchun ishlatiladi
        if not user:
            return Response({"detail": "Bunday telefon raqamga ega foydalanuvchi topilmadi."}, status=404)
        
        # now = timezone.now() - timedelta(minutes=1)  # 1 daqiqadan eski kodlarni tekshirish uchun vaqtni belgilaymiz, bu eski kodlarni tekshirish uchun ishlatiladi
        now = timezone.now()

        if user.otp_created_at:
            # time_passedda biz userning otp_created_at va hozirgi vaqt orasidagi farqni hisoblaymiz, 
            # bu otp kodining amal qilish muddatini tekshirish uchun ishlatiladi
            time_passed = now - user.otp_created_at

            # agar userning otp_attempts 3 yoki undan ko'p bo'lsa va time_passed 1 soatdan kam bo'lsa, xato javob qaytaradi, 
            # bu yerda 429 Too Many Requests status kodi ishlatiladi, bu foydalanuvchi juda ko'p so'rov yuborganligini bildiradi
            if user.otp_attempts >= 3 and time_passed < timedelta(hours=1):
                # buyerda biz userga qancha vaqt qolganligini ko'rsatamiz, bu foydalanuvchiga qancha vaqt kutish kerakligini ko'rsatish uchun ishlatiladi
                remaining = timedelta(hours=1) - time_passed
                return Response({"detail": f"Ko'p urinishlar. Iltimos, {remaining.seconds // 60} daqiqadan keyin qaytadan urinib ko'ring."}, status=429)
            
            # agar time_passed 30 sekunddan ko'p bo'lsa, userning otp_attempts ni 0 ga tenglaymiz, bu foydalanuvchiga yangi kod yuborish uchun imkon beradi, 
            # bu yerda 30 sekundlik vaqt chegarasi qo'yilgan, bu foydalanuvchiga yangi kod yuborish uchun kutish kerakligini bildiradi
            if time_passed < timedelta(seconds=30):
                # remaining vazifasi userga yangi kod yuborish uchun qancha vaqt kutish kerakligini ko'rsatish uchun ishlatiladi, 
                # bu foydalanuvchiga yangi kod yuborish uchun kutish kerakligini bildiradi
                remaining = timedelta(seconds=30) - time_passed
                return Response({"detail": f"Yangi kod yuborish uchun {remaining.seconds} sekund kuting."}, status=429)
            
            # agar time_passed 1 soatdan ko'p bo'lsa, userning otp_attempts ni 0 ga tenglaymiz, bu foydalanuvchiga yangi kod yuborish uchun imkon beradi,
            if time_passed >= timedelta(hours=1):
                user.otp_attempts = 0

        #bu yerda send_eskiz_sms funksiyasini chaqiramiz, bu funksiya telefon raqamga sms yuboradi va tasdiqlash kodini qaytaradi, 
        # agar sms yuborish muvaffaqiyatli bo'lsa, tasdiqlash kodini user modelida saqlaymiz, bu tasdiqlash kodini keyinchalik tekshirish uchun ishlatiladi
        code = send_eskiz_sms(phone_number)
        #agar code mavjud bo'lsa, user modelida tasdiqlash kodini saqlaymiz, bu tasdiqlash kodini keyinchalik tekshirish uchun ishlatiladi
        if code:
            # bunda userning verification_code atributiga code ni saqlaymiz, bu tasdiqlash kodini keyinchalik tekshirish uchun ishlatiladi
            user.verification_code = code
            # userning otp_created_at atributiga hozirgi vaqtni saqlaymiz, bu tasdiqlash kodining amal qilish muddatini tekshirish uchun ishlatiladi
            user.otp_created_at = now
            # buyerda esa userning otp_attempts ni 1 ga oshiramiz, bu foydalanuvchining kodni noto'g'ri kiritganligini bildiradi
            user.otp_attempts += 1
            user.save()
            return Response({"detail": "Tasdiqlash kodi yuborildi."}, status=200)
        else:
            return Response({"detail": "Tasdiqlash kodida xatolik."}, status=500)
            

# AdminCreateLoginAPIView maqsadi admin yaratish va login qilish, bu yerda admin yaratish va login qilish uchun ishlatiladi
class AdminCreateLoginAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: SellerCreateSerializer(many=True)},tags=['Admin'])
    def get(self, request):
        products = User.objects.all().order_by('-id')
        serializer = SellerCreateSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    

    @swagger_auto_schema(request_body=SellerCreateSerializer, tags=['Admin'])
    # post yaratishimiz uchun funksiya yaratamiz va admin yaratamiz
    def post(self, request, *args, **kwargs):
        # serializerdan ma'lumotlarni olish uchun serializerni yaratamiz va request.data ni unga beramiz, bu serializer admin yaratish uchun ishlatiladi
        serializer = SellerCreateSerializer(data=request.data)

        if not serializer.is_valid():
            # agar serializer valid bo'lmasa, xato javob qaytaradi, bu yerda 400 Bad Request status kodi ishlatiladi, bu foydalanuvchi noto'g'ri ma'lumot yuborganligini bildiradi
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']

        # user yaratishimizda bazada yanii userlar ichida shu nomder bormi yuqmi deb filter qilib tekshirib olamiz
        user = User.objects.filter(phone_number=phone_number).first()

        if user:
            # agar user topilsa, userning rolini o'qituvchi sifatida yangilaymiz, parolni yangilaymiz va userni faollashtiramiz, 
            # bu yerda mavjud foydalanuvchi o'qituvchi sifatida yangilanadi
            user.role = User.Role.TEACHER
            user.password = make_password(password)
            user.is_active = True
            user.save()
            message = "Mavjud foydalanuvchi o'qituvchi sifatida yangilandi."

        else:
            # Yangi foydalanuvchi yaratish (Bu qismda message yo'q edi)
            user = User.objects.create(
                phone_number=phone_number,
                password=make_password(password),
                role=User.Role.TEACHER,
                is_active=True
            )
            message = "Yangi foydalanuvchi o'qituvchi sifatida yaratildi."
        # agar user topilmasa, yangi user yaratamiz, bu yerda yangi foydalanuvchi o'qituvchi sifatida yaratiladi
        return Response({
            "message": message,
            "login": phone_number,
            "role": user.role
            }, status=status.HTTP_200_OK if user else status.HTTP_201_CREATED)      

class AdminListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Admin'])
    def get(self, request, pk):
        try:
            product = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SellerCreateSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(tags=['Admin'])
    def delete(self, request, pk):
        try:
            product = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response({"message": "User o'chirildi"})
     
    
# NewPassworAPIView maqsadi token orqali kirgan foydalanuvchining parolini yangilash, bu yerda token orqali kirgan foydalanuvchining parolini yangilash uchun ishlatiladi
class NewPassworAPIView(APIView):
    # permission bizda token orqali kirganlar foydalanishini belgilab beradi
    permission_classes = [AllowAny]
    # authentication_classes ni JWTAuthentication ga tenglaymiz, bu yerda JWTAuthentication tokenni tekshirish uchun ishlatiladi
    # maqsadi token orqali kirgan foydalanuvchining haqiqatan ham tokenni tekshirish va unga ruxsat berish uchun ishlatiladi
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=SetNewPasswordSerializer, tags=['Auth'])
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        # agar serializer valid bo'lmasa, xato javob qaytaradi, bu yerda 400 Bad Request status kodi ishlatiladi, bu foydalanuvchi noto'g'ri ma'lumot yuborganligini bildiradi
        serializer.is_valid(raise_exception=True)

        # rquset.user orqali token orqali kirgan foydalanuvchini olamiz, bu yerda request.user token orqali kirgan foydalanuvchini olish uchun ishlatiladi
        # maqsadi token orqali kirgan foydalanuvchining haqiqatan ham tokenni tekshirish va unga ruxsat berish uchun ishlatiladi
        user = request.user
        # user.set_password() metodi userning parolini yangilash uchun ishlatiladi, bu yerda serializer.validated_data['new_password'] yangi parolni olish uchun ishlatiladi.
        user.set_password(serializer.validated_data['new_password'])

        # buyerdagi 3 ta funksiyada userning verification_code ni None ga tenglaymiz, otp_attempts ni 0 ga tenglaymiz va userni saqlaymiz, bu yerda parolni yangilashdan keyin userning tasdiqlash kodini o'chirish va urinishlar sonini 0 ga tenglash uchun ishlatiladi
        user.verification_code = None
        user.otp_attempts = 0
        user.save()

        return Response({"detail": "Parol muvaffaqiyatli yangilandi."}, status=status.HTTP_200_OK)
    

# CreatePasswordAPIView maqsadi foydalanuvchining tasdiqlash kodini tekshirish va agar kod to'g'ri bo'lsa, unga yangi parol o'rnatish imkoniyatini berish, bu yerda tasdiqlash kodini tekshirish va yangi parol o'rnatish uchun ishlatiladi
class CreatePasswordAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=VerifyOTPSerializer, tags=['Auth'])
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        user = User.objects.filter(phone_number = phone_number).first()
        if not user:
            return Response({"detail": "Code yoki Raqam xato, iltimos tekshiring."}, status=404)
        
        if user.otp_created_at and timezone.now() - user.otp_created_at > timedelta(minutes=1):
            return Response({"detail": "Code eskirgan, iltimos yangi code oling."}, status=400)
        
        # refresh orqali token yaratish uchun RefreshToken.for_user() metodidan foydalanamiz, bu metod user ni qabul qiladi va refresh tokenni yaratadi, bu yerda token yaratish uchun ishlatiladi
        # maqsadi token orqali kirgan foydalanuvchining haqiqatan ham tokenni tekshirish va unga ruxsat berish uchun ishlatiladi, bu yerda token yaratish uchun ishlatiladi
        refresh = RefreshToken.for_user(user)

        response = Response({
            "message": "Kod tasdiqlandi. Endi yangi parolni o'rnating.",
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)

        # buyerda refresh tokenni cookiega saqlaymiz, bu refresh tokenni keyinchalik ishlatish uchun, masalan, access tokenni yangilashda refresh tokenni tekshirish uchun ishlatiladi, 
        # bu yerda refresh tokenni cookiega saqlash uchun ishlatiladi
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax',        
        )
        return response
    

# RefreshTokenAPIView maqsadi access tokenni yangilash uchun refresh tokenni tekshirish va yangi access tokenni yaratish, bu yerda access tokenni yangilash uchun refresh tokenni tekshirish va yangi access tokenni yaratish uchun ishlatiladi
class RefreshTokenAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['Auth'])
    def post(self, request):
        # auth_headr orqali Authorization headerini olish uchun request.headers.get() metodidan foydalanamiz, bu yerda Authorization headerini olish uchun ishlatiladi
        # maqsadi tokenni yangilashda refresh tokenni tekshirish uchun ishlatiladi, bu yerda Authorization headerini olish uchun ishlatiladi
        auth_headr = request.headers.get('Authorization')

        # agar Authorization header topilmasa, xato javob qaytaradi, bu yerda 400 Bad Request status kodi ishlatiladi, bu foydalanuvchi Authorization headerini yubormaganligini bildiradi
        if not auth_headr:
            return Response({"detail": "Authorization header topilmadi."}, status=status.HTTP_400_BAD_REQUEST)
        
        # buyerda refresh tokenni cookiedan olish uchun request.COOKIES.get() metodidan foydalanamiz, bu yerda refresh tokenni cookiedan olish uchun ishlatiladi
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({"detail": "Refresh token topilmadi."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)   
        
        except (TokenError, InvalidToken):
            return Response({"detail": "Refresh token xato yoki eskirgan."}, status=status.HTTP_401_UNAUTHORIZED)
        