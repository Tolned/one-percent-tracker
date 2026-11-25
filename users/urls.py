from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserProfileAPIView, UserRegisterAPIView

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", UserProfileAPIView.as_view(), name="profile"),
]