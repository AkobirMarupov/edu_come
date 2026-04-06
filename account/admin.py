from django.contrib import admin
from .models import User
from django.contrib.auth.hashers import make_password

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
 
    list_display = ('id', 'phone_number', 'telegram_id', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('phone_number', 'telegram_id')

    fields = ('phone_number', 'password', 'telegram_id', 'role', 'is_active', 'is_staff', 'is_superuser')

    def save_model(self, request, obj, form, change):
        
        if obj.password and not obj.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)