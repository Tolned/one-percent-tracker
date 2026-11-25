from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Habit(models.Model):
    """Модель привычки на основе концепции "Атомных привычек"."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место выполнения",
        help_text="Место, в котором необходимо выполнять привычку",
    )
    time = models.TimeField(
        verbose_name="Время выполнения",
        help_text="Время, когда необходимо выполнять привычку",
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Действие, которое представляет собой привычка",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Привычка, которую можно привязать к выполнению полезной привычки",
    )
    associated_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="associated_by",
        verbose_name="Связанная привычка",
        help_text="Привычка, которая связана с другой привычкой (только приятные)",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность (в днях)",
        help_text="Периодичность выполнения привычки для напоминания (1-7 дней)",
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Чем пользователь должен себя вознаградить после выполнения",
    )
    execution_time = models.PositiveIntegerField(
        default=120,
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name="Время на выполнение (в секундах)",
        help_text="Время, которое предположительно потратит пользователь (не более 120 секунд)",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text="Привычки можно публиковать в общий доступ",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} в {self.time} ({self.place})"
