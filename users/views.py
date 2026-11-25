from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer, UserSerializer

User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    """Регистрация: создаёт пользователя и сразу выдаёт пару JWT-токенов."""

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    @extend_schema(
        summary="Регистрация пользователя",
        description="Создаёт пользователя по email и паролю. Возвращает данные профиля и JWT-токены.",
        request=UserRegisterSerializer,
        responses={
            201: OpenApiResponse(description="Пользователь создан, возвращены токены"),
            400: OpenApiResponse(description="Ошибка валидации (email занят, короткий пароль и т.п.)"),
        },
        tags=["Авторизация"],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """Профиль текущего пользователя: просмотр и редактирование."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        summary="Профиль текущего пользователя",
        responses={200: UserSerializer, 401: OpenApiResponse(description="Не авторизован")},
        tags=["Авторизация"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление профиля",
        description="Позволяет указать telegram_chat_id для получения напоминаний.",
        request=UserSerializer,
        responses={200: UserSerializer, 400: OpenApiResponse(description="Ошибка валидации")},
        tags=["Авторизация"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление профиля",
        request=UserSerializer,
        responses={200: UserSerializer},
        tags=["Авторизация"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)