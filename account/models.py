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

    phone_number = models.CharField(max_length=20, unique=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_attempts = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.phone_number