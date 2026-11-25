from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Пользователь может редактировать/удалять только свои привычки.
    Для остальных действий (GET, HEAD, OPTIONS) доступ разрешен.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in SAFE_METHODS:
            return True

        # Разрешаем изменение/удаление только владельцу
        return obj.user == request.user


class IsPublicReadOnly(BasePermission):
    """
    Доступ к публичным привычкам только для чтения.
    """

    def has_permission(self, request, view):
        # Разрешаем только безопасные методы
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        # Разрешаем только если привычка публичная
        return obj.is_public and request.method in SAFE_METHODS
