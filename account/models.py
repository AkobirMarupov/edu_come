from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from common.models import BaseModel
from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        STUDENT = 'student', _('Student')
        TEACHER = 'teacher', _('Teacher')


    phone_number = models.CharField(max_length=20, unique=True, verbose_name=_("Telefon raqami"))
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Ism"))
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Familiya"))
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name=_("Profil rasmi"))
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT, verbose_name=_("Rol"))
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_attempts = models.IntegerField(default=0)
    telegram_username = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text=_("Telegram userneymingiz (masalan: @akobir_dev)"),
        verbose_name=_("Telegram havola")
    )
    bio = models.TextField(blank=True, null=True, verbose_name=_("O'zi haqida qisqacha"))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = _('Foydalanuvchi')
        verbose_name_plural = _('Foydalanuvchilar')

    def __str__(self):
        return f"{self.phone_number} ({self.get_role_display()})"

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.phone_number