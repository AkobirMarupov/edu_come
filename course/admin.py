from django.contrib import admin
from .models import Category, SubCategory, Course, Lesson



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
    autocomplete_fields = ('category', 'parent')


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['title', 'description', 'video_url', 'video_file', 'duration_display']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # 'owner'ni ham ro'yxatda ko'rsatamiz
    list_display = ['title', 'price', 'sub_category', 'owner']
    search_fields = ['title', 'sub_category']
    list_filter = ['sub_category']
    exclude = ['owner',]
    
    inlines = [LessonInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not change: # Yangi yaratilayotgan bo'lsa
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'duration_display']
    list_filter = ['course']
    search_fields = ['title']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(course__owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course" and not request.user.is_superuser:
            kwargs["queryset"] = Course.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)