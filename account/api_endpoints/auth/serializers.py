from rest_framework import serializers  # Django REST Framework serializerlari
from django.contrib.auth import authenticate  # foydalanuvchi autentifikatsiyasi uchun


class CheckPhoneSerializer(serializers.Serializer):
    # Telefon raqamni tekshirish uchun serializer
    phone_number = serializers.CharField(max_length=15)  # maksimal 15 ta belgi bo'lishi kerak


class SellerCreateSerializer(serializers.Serializer): 
    # Seller (sotuvchi) yaratish uchun serializer
    phone_number = serializers.CharField(max_length=15)  # telefon raqam maydoni
    password = serializers.CharField(min_length=8, write_only=True)  # parol maydoni, faqat kirish uchun

    def validate_phone_number(self, value):
        # telefon raqam faqat raqamlardan iborat ekanligini tekshiradi
        if not value.replace('+', '').isdigit():
            raise serializers.ValidationError("Telefon raqam faqat raqamlardan iborat bo'lishi kerak.")
        return value  # to'g'ri bo'lsa qiymatni qaytaradi
    


class VerifyOTPSerializer(serializers.Serializer):
    # OTP kodni tasdiqlash uchun serializer
    phone_number = serializers.CharField()  # telefon raqam maydoni
    code = serializers.CharField()  # yuborilgan kod maydoni


class SetNewPasswordSerializer(serializers.Serializer):
    # Yangi parol o'rnatish uchun serializer
    new_password = serializers.CharField()  # yangi parol maydoni

    def validate(self, data):
        # umumiy tekshiruv, hozircha faqat data ni qaytaradi
        return data
    

class LoginSerializer(serializers.Serializer):
    # Login qilish uchun serializer
    phone_number = serializers.CharField(max_length=15)  # telefon raqam maydoni
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})  # parol maydoni

    def validate(self, data):
        # kelgan ma'lumotlarni tekshiradi
        phone_number = data.get('phone_number')  # telefonni oladi
        password = data.get('password')  # parolni oladi

        if phone_number and password:
            # agar telefon va parol bo'lsa, authenticate bilan tekshiradi
            user = authenticate(request=self.context.get('request'),
                                username=phone_number, 
                                password=password)

            if not user:
                # foydalanuvchi topilmasa xato chiqaradi
                raise serializers.ValidationError(
                    "Telefon raqam yoki parol xato. Qaytadan urinib ko'ring."
                )
            
            if not user.is_active:
                # hisob faol emas bo'lsa xato chiqaradi
                raise serializers.ValidationError("Ushbu hisob faol emas.")
        else:
            # agar telefon yoki parol bo'lmasa xato beradi
            raise serializers.ValidationError("Telefon raqam va parolni kiritish shart.")

        data['user'] = user  # tekshirilgan foydalanuvchi obyektini qo'shadi
        return data  # natijaviy ma'lumotni qaytaradi
