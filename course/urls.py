from django.urls import path
from course.apps import CourseConfig
from rest_framework.routers import DefaultRouter
from course.views import (CourseViewSet,
                          LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView
                        )

app_name = CourseConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name= 'lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name= 'lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name= 'lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name= 'lesson-update'),
    path('lesson/delet/<int:pk>/', LessonDestroyAPIView.as_view(), name= 'lesson-delet'),
    
] + router.urls