from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserCreateAPIView, MyTokenObtainPairView
from users.apps import UsersConfig
app_name = UsersConfig.name

urlpatterns = [
    path("createuser/", UserCreateAPIView.as_view(), name="createuser"),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]