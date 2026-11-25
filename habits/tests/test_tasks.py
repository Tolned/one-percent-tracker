import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from habits.tasks import send_habit_reminders
from habits.models import Habit


@pytest.mark.django_db
@patch("habits.tasks.requests.post")
def test_send_habit_reminders_success(mock_post, user):
    # Создаем привычку, которая должна сработать прямо сейчас
    now = timezone.now()
    habit = Habit.objects.create(
        user=user,
        place="Кухня",
        time=now.time(),
        action="Выпить воду",
        execution_time=60,
        periodicity=1,
        reward="Похвалить себя"
    )

    # Настраиваем мок ответа
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    # Вызываем задачу
    send_habit_reminders()

    # Проверяем, что requests.post был вызван 1 раз
    assert mock_post.call_count == 1

    # Проверяем аргументы вызова
    call_args = mock_post.call_args
    assert call_args.kwargs["json"]["chat_id"] == "123456789"
    assert "Выпить воду" in call_args.kwargs["json"]["text"]
    assert "Похвалить себя" in call_args.kwargs["json"]["text"]


@pytest.mark.django_db
@patch("habits.tasks.requests.post")
def test_send_habit_reminders_no_chat_id(mock_post, user):
    user.telegram_chat_id = None
    user.save()

    now = timezone.now()
    Habit.objects.create(
        user=user,
        place="Кухня",
        time=now.time(),
        action="Выпить воду",
        execution_time=60,
        periodicity=1
    )

    send_habit_reminders()

    # Запрос не должен был быть отправлен, т.к. нет chat_id
    assert mock_post.call_count == 0