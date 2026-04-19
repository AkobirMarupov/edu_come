from django.urls import path
from course.api_endpoints.category.views import (
        CategoryListAPIView, CategoryDetailAPIView, SubCategoryListAPIView, SubCategoryDetailAPIView)
from course.api_endpoints.lesson.views import (
        CourseListAPIView, CourseDetailAPIView, LessonListAPIView, LessonDetailAPIView)
from course.api_endpoints.application.application_views import CourseApplicationListAPIView, CourseApplicationApproveAPIView


urlpatterns = [
    #subcategory
    path('subcategory/', SubCategoryListAPIView.as_view(), name='subcategory-create'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory-detail'),
    #category
    path('categories/', CategoryListAPIView.as_view(), name='category-create'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    #course
    path('course/', CourseListAPIView.as_view(), name='course-create'),
    path('course/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    #lesson
    path('lesson/', LessonListAPIView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson-detail'),

    path('applications/', CourseApplicationListAPIView.as_view()),
    path('applications/<int:pk>/approve/', CourseApplicationApproveAPIView.as_view()),

]