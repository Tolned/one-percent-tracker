from rest_framework import serializers

from .models import Habit
from .validators import (
    validate_associated_habit,
    validate_execution_time,
    validate_habit_consistency,
    validate_not_self_reference,
    validate_periodicity,
)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки с полным набором валидаторов из ТЗ."""

    execution_time = serializers.IntegerField(
        required=False,
        default=120,
        min_value=1,
        max_value=120,
        validators=[validate_execution_time],
        help_text="Время на выполнение в секундах (не более 120).",
    )
    periodicity = serializers.IntegerField(
        required=False,
        default=1,
        min_value=1,
        max_value=7,
        validators=[validate_periodicity],
        help_text="Периодичность выполнения в днях (от 1 до 7).",
    )

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "associated_habit",
            "periodicity",
            "reward",
            "execution_time",
            "is_public",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        # Связать можно только свою привычку — чужие недоступны
        if request is not None and request.user.is_authenticated:
            self.fields["associated_habit"].queryset = Habit.objects.filter(user=request.user)

    def _current_value(self, attrs, field, default=None):
        """Значение поля с учётом уже сохранённых данных (важно для PATCH)."""
        if field in attrs:
            return attrs[field]
        if self.instance is not None:
            return getattr(self.instance, field)
        return default

    def validate(self, attrs):
        is_pleasant = self._current_value(attrs, "is_pleasant", False)
        reward = self._current_value(attrs, "reward")
        associated_habit = self._current_value(attrs, "associated_habit")

        validate_associated_habit(associated_habit)
        validate_not_self_reference(self.instance, associated_habit)
        validate_habit_consistency(
            is_pleasant=is_pleasant,
            reward=reward,
            associated_habit=associated_habit,
        )
        return attrs


class HabitPublicSerializer(serializers.ModelSerializer):
    """Сериализатор публичных привычек — только чтение, без данных владельца."""

    class Meta:
        model = Habit
        fields = [
            "id",
            "place",
            "time",
            "action",
            "is_pleasant",
            "associated_habit",
            "periodicity",
            "reward",
            "execution_time",
            "is_public",
        ]
        read_only_fields = fields