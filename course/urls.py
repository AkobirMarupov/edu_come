from django.urls import path
from course.api_endpoints.category.views import (
        CategoryListAPIView, CategoryDetailAPIView, MySubCategoryListAPIView, 
        SubCategoryDetailAPIView, MyCategoryAPIView, SubCategoryListAPIView)
from course.api_endpoints.lesson.views import (
        CourseListAPIView, CourseDetailAPIView, LessonListAPIView, LessonDetailAPIView,
        MyCourseListAPIView, MyLessonListAPIView)
from course.api_endpoints.application.application_views import CourseApplicationListAPIView, CourseApplicationApproveAPIView
from course.api_endpoints.review.views import EnrollmentAPIVIew, EnrollmentDetailAPIVIew

urlpatterns = [
    #subcategory
    path('subcat/', SubCategoryListAPIView.as_view(), name='subcategory'),
    path('subcategory/', MySubCategoryListAPIView.as_view(), name='subcategory-create'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory-detail'),
    #category
    path('categori/', MyCategoryAPIView.as_view(), name='category-create'),
    path('categories/', CategoryListAPIView.as_view(), name='category'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    #course
    path('courses/', CourseListAPIView.as_view(), name='course-create'),
    path('course/', MyCourseListAPIView.as_view(), name='course-create'),
    path('course/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    #lesson
    path('lessons/', LessonListAPIView.as_view(), name='lesson-create'),
    path('lesson/', MyLessonListAPIView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson-detail'),

    path('applications/', CourseApplicationListAPIView.as_view()),
    path('applications/<int:pk>/', CourseApplicationApproveAPIView.as_view()),

    path('enrollments/', EnrollmentAPIVIew.as_view(), name='enroliment'),
    path('enrollments/<int:pk>/', EnrollmentDetailAPIVIew.as_view(), name='enrol-detail'),


]