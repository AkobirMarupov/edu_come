from django.contrib import admin
from .models import User
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'full_name', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (_('Asosiy ma’lumotlar'), {
            'fields': ('phone_number', 'password', 'role')
        }),
        (_('Shaxsiy ma’lumotlar'), {
            'fields': ('first_name', 'last_name', 'avatar', 'telegram_username', 'bio')
        }),
        (_('Huquqlar va Status'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Muhim sanalar'), {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    readonly_fields = ('date_joined', 'last_login')

    def save_model(self, request, obj, form, change):
        """Parolni xavfsiz saqlash (hash qilish) mantiqi"""
        if obj.password and not obj.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = _('Ism-familiya')