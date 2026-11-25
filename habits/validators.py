"""Валидаторы привычек согласно ТЗ проекта «Атомные привычки»."""

from rest_framework import serializers

MAX_EXECUTION_TIME = 120  # секунд — правило двух минут
MIN_PERIODICITY = 1  # день
MAX_PERIODICITY = 7  # дней — не реже раза в неделю


def validate_execution_time(value):
    """Время выполнения должно быть от 1 до 120 секунд."""
    if value is None:
        return value
    if value < 1:
        raise serializers.ValidationError("Время выполнения должно быть не меньше 1 секунды.")
    if value > MAX_EXECUTION_TIME:
        raise serializers.ValidationError(
            f"Время выполнения должно быть не больше {MAX_EXECUTION_TIME} секунд."
        )
    return value


def validate_periodicity(value):
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней."""
    if value is None:
        return value
    if value < MIN_PERIODICITY:
        raise serializers.ValidationError(f"Периодичность должна быть не меньше {MIN_PERIODICITY} дня.")
    if value > MAX_PERIODICITY:
        raise serializers.ValidationError(
            f"Нельзя выполнять привычку реже, чем 1 раз в {MAX_PERIODICITY} дней."
        )
    return value


def validate_associated_habit(habit):
    """В связанные привычки могут попадать только приятные привычки."""
    if habit is None:
        return habit
    if not habit.is_pleasant:
        raise serializers.ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки."
        )
    return habit


def validate_habit_consistency(*, is_pleasant, reward, associated_habit):
    """
    Проверка взаимосвязанных полей привычки:
    - нельзя одновременно указать вознаграждение и связанную привычку;
    - у приятной привычки не может быть ни вознаграждения, ни связанной привычки.
    """
    errors = {}

    if reward and associated_habit:
        errors["associated_habit"] = (
            "Нельзя одновременно указать связанную привычку и вознаграждение. "
            "Выберите только одно из двух."
        )

    if is_pleasant:
        if reward:
            errors["reward"] = "У приятной привычки не может быть вознаграждения."
        if associated_habit:
            errors["associated_habit"] = "У приятной привычки не может быть связанной привычки."

    if errors:
        raise serializers.ValidationError(errors)


def validate_not_self_reference(instance, associated_habit):
    """Привычка не может быть связана сама с собой."""
    if associated_habit is None or instance is None:
        return
    if associated_habit.pk == instance.pk:
        raise serializers.ValidationError(
            {"associated_habit": "Привычка не может быть связана сама с собой."}
        )