from django.db import models
from common.models import BaseModel
from django.conf import settings
import os


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class SubCategory(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='subcategories')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children')

    def __str__(self):
        return self.name


class Course(BaseModel):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses', verbose_name="Muallif")
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Lesson (BaseModel):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to='lessons/videos/', blank=True, null=True)
    duration_display = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.course.title} - {self.title}"