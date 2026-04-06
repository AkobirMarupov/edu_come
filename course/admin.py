from django.contrib import admin
from .models import Category, SubCategory


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'parent', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('-created_at',)

    # 🔥 Dropdownni yaxshilash
    autocomplete_fields = ('category', 'parent')