from rest_framework import serializers


def validate_habit(data):
    """
    Кастомный валидатор для модели Habit.
    Проверяет все требования из ТЗ.
    """
    is_pleasant = data.get("is_pleasant", False)
    reward = data.get("reward")
    associated_habit = data.get("associated_habit")
    execution_time = data.get("execution_time", 120)
    periodicity = data.get("periodicity", 1)

    # 1. Нельзя одновременно указать связанную привычку и вознаграждение
    if reward and associated_habit:
        raise serializers.ValidationError(
            "Нельзя одновременно указать связанную привычку и вознаграждение. " "Выберите только одно из двух."
        )

    # 2. Время выполнения должно быть не больше 120 секунд
    if execution_time > 120:
        raise serializers.ValidationError("Время выполнения должно быть не больше 120 секунд.")

    # 3. В связанные привычки могут попадать только привычки с признаком приятной
    if associated_habit and not associated_habit.is_pleasant:
        raise serializers.ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки."
        )

    # 4. У приятной привычки не может быть вознаграждения или связанной привычки
    if is_pleasant:
        if reward:
            raise serializers.ValidationError("У приятной привычки не может быть вознаграждения.")
        if associated_habit:
            raise serializers.ValidationError("У приятной привычки не может быть связанной привычки.")

    # 5. Нельзя выполнять привычку реже, чем 1 раз в 7 дней
    if periodicity > 7:
        raise serializers.ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")

    return data
