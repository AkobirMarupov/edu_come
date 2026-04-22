from django.contrib import admin
from .models import Notification, HeroBanner

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'title')
    readonly_fields = ('created_at',)


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    # Asosiy ro'yxatda nimalar chiqsin
    list_display = ('title', 'is_active', 'courses_count_text', 'students_count_text', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    fieldsets = (
        ("Asosiy matnlar", {
            'fields': ('title', 'subtitle')
        }),
        ("Statistika ma'lumotlari", {
            'fields': (('courses_count_text', 'students_count_text', 'rating_text'),) 
        }),
        ("Dizayn va Holat", {
            'fields': ('background_gradient', 'image', 'is_active')
        }),
    )

    search_fields = ('title', 'subtitle')