from django.urls import path
from course.apps import CourseConfig
from rest_framework.routers import DefaultRouter
from course.views import (CourseViewSet,
                          LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView,
                          PaymentListAPIView,
                          SubscriptionCreateAPIView, SubscriptionDestroyAPIView, SubscriptionListAPIView, SubscriptionRetrieveAPIView, SubscriptionUpdateAPIView
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
    path("payment/", PaymentListAPIView.as_view(), name="PAY"),

    path("user/sub/create/", SubscriptionCreateAPIView.as_view(), name="subscription_create"),
    path("user/sub/list/", SubscriptionListAPIView.as_view(), name="subscription_list"),
    path("user/sub/deteil/<int:pk>/", SubscriptionRetrieveAPIView.as_view(), name="subscription_deteil"),
    path("user/sub/update/<int:pk>/", SubscriptionUpdateAPIView.as_view(), name="subscription_update"),
    path("user/sub/delete/<int:pk>/", SubscriptionDestroyAPIView.as_view(), name="subscription_delete"),
    
] + router.urls