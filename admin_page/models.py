from django.db import models

from common.models import BaseModel
from account.models import User


class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)


class HeroBanner(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Asosiy sarlavha",
        help_text="Masalan: O'zbekistondagi Eng Yaxshi Online Ta'lim Platformasi")
    subtitle = models.TextField(verbose_name="Kichik matn",
        help_text="Sarlavha ostidagi tushuntirish matni")    
    courses_count_text = models.CharField(max_length=50,  default="6+", 
        verbose_name="Kurslar soni matni")
    students_count_text = models.CharField(max_length=50, default="670+", 
        verbose_name="O'quvchilar soni matni")
    rating_text = models.CharField(max_length=50, default="4.8", 
        verbose_name="Reyting matni")
    background_gradient = models.CharField(max_length=100, default="linear-gradient(90deg, #6A11CB 0%, #2575FC 100%)",
        verbose_name="Fon gradiyenti (CSS)")
    image = models.ImageField(upload_to='banners/', blank=True, null=True, 
        verbose_name="Banner rasmi (ixtiyoriy)")
    is_active = models.BooleanField(default=True, verbose_name="Saytda ko'rinsinmi?")

    class Meta:
        verbose_name = "Asosiy Banner"
        verbose_name_plural = "Asosiy Bannerlar"

    def __str__(self):
        return self.title