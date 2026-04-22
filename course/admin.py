from django.contrib import admin
from .models import (
    Category, SubCategory, Course, 
    Lesson, CourseApplication, Enrollment, Review, Wishlist
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'parent', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'price', 'created_at', 'image')
    list_filter = ('category', 'owner')
    search_fields = ('title', 'description')
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration_display', 'is_preview')
    list_filter = ('course', 'is_preview')
    search_fields = ('title', 'description')

@admin.register(CourseApplication)
class CourseApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__phone_number', 'course__title')
    actions = ['approve_applications', 'reject_applications']

    @admin.action(description="Tanlangan arizalarni tasdiqlash")
    def approve_applications(self, request, queryset):
        for app in queryset:
            app.status = 'approved'
            app.save()
            Enrollment.objects.get_or_create(user=app.user, course=app.course)
        self.message_user(request, "Arizalar tasdiqlandi va talabalar kursga qo'shildi.")

    @admin.action(description="Tanlangan arizalarni rad etish")
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('course',)
    search_fields = ('user__phone_number', 'course__title')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'course')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')