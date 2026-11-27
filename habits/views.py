from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Habit
from .permissions import IsOwnerOrReadOnly, IsPublicReadOnly
from .serializers import HabitPublicSerializer, HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD привычек текущего пользователя. Список отдаётся с пагинацией по 5 элементов."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "time"]
    ordering = ["-created_at"]

    def get_queryset(self):
        # Защита при генерации схемы drf-spectacular (запрос без авторизации)
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.none()
        return Habit.objects.filter(user=self.request.user).select_related("associated_habit")

    def perform_create(self, serializer):
        """Автоматически присваиваем текущего пользователя владельцем привычки."""
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Список привычек текущего пользователя",
        description="Возвращает привычки текущего пользователя. Пагинация limit/offset, по 5 на страницу.",
        responses={200: HabitSerializer(many=True), 401: OpenApiResponse(description="Не авторизован")},
        tags=["Привычки"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание привычки",
        description="Создаёт привычку. Владелец подставляется автоматически из токена.",
        request=HabitSerializer,
        responses={
            201: HabitSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            401: OpenApiResponse(description="Не авторизован"),
        },
        tags=["Привычки"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение привычки",
        responses={
            200: HabitSerializer,
            404: OpenApiResponse(description="Привычка не найдена или принадлежит другому пользователю"),
        },
        tags=["Привычки"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Полное обновление привычки",
        request=HabitSerializer,
        responses={200: HabitSerializer, 400: OpenApiResponse(description="Ошибка валидации")},
        tags=["Привычки"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление привычки",
        request=HabitSerializer,
        responses={200: HabitSerializer, 400: OpenApiResponse(description="Ошибка валидации")},
        tags=["Привычки"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление привычки",
        responses={204: OpenApiResponse(description="Привычка удалена")},
        tags=["Привычки"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """Список публичных привычек — доступен всем, только чтение."""

    serializer_class = HabitPublicSerializer
    permission_classes = [IsPublicReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "time"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).select_related("associated_habit")

    @extend_schema(
        summary="Список публичных привычек",
        description="Общий список привычек, открытых владельцами. Редактирование недоступно.",
        responses={200: HabitPublicSerializer(many=True)},
        tags=["Публичные привычки"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получение публичной привычки",
        responses={200: HabitPublicSerializer, 404: OpenApiResponse(description="Привычка не найдена")},
        tags=["Публичные привычки"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)