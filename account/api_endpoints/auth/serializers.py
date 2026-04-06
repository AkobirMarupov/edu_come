from rest_framework import serializers
from django.contrib.auth import authenticate


class CheckPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)


class SellerCreateSerializer(serializers.Serializer): 
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_phone_number(self, value):
        if not value.replace('+', '').isdigit():
            raise serializers.ValidationError("Telefon raqam faqat raqamlardan iborat bo'lishi kerak.")
        return value
    

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()

    def validate(self, data):
        return data
    
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = authenticate(request=self.context.get('request'),
                                username=phone_number, 
                                password=password)

            if not user:
                raise serializers.ValidationError(
                    "Telefon raqam yoki parol xato. Qaytadan urinib ko'ring."
                )
            
            if not user.is_active:
                raise serializers.ValidationError("Ushbu hisob faol emas.")
        else:
            raise serializers.ValidationError("Telefon raqam va parolni kiritish shart.")

        data['user'] = user
        return data