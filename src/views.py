from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Habit
from .serializers import HabitSerializer, HabitPublicSerializer
from .permissions import IsOwnerOrReadOnly, IsPublicReadOnly


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с привычками текущего пользователя.
    Поддерживает полный CRUD.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "time"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Возвращаем только привычки текущего пользователя."""
        return Habit.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Список привычек текущего пользователя",
        description="Возвращает список всех привычек текущего пользователя с пагинацией (5 на страницу).",
        responses={200: HabitSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание привычки",
        description="Создает новую привычку для текущего пользователя.",
        request=HabitSerializer,
        responses={201: HabitSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение привычки",
        description="Возвращает детали конкретной привычки.",
        responses={200: HabitSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление привычки",
        description="Полностью обновляет привычку.",
        request=HabitSerializer,
        responses={200: HabitSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление привычки",
        description="Частично обновляет привычку.",
        request=HabitSerializer,
        responses={200: HabitSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление привычки",
        description="Удаляет привычку.",
        responses={204: OpenApiResponse(description="Привычка удалена")},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра публичных привычек (только чтение).
    """

    serializer_class = HabitPublicSerializer
    permission_classes = [IsPublicReadOnly]
    queryset = Habit.objects.filter(is_public=True)

    @extend_schema(
        summary="Список публичных привычек",
        description="Возвращает список всех публичных привычек с пагинацией.",
        responses={200: HabitPublicSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получение публичной привычки",
        description="Возвращает детали конкретной публичной привычки.",
        responses={200: HabitPublicSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
