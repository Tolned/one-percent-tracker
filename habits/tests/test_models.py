import pytest
from django.core.exceptions import ValidationError
from habits.models import Habit
from django.utils import timezone


@pytest.mark.django_db
def test_habit_creation(habit):
    assert habit.action == "Выпить стакан воды"
    assert habit.execution_time == 60


@pytest.mark.django_db
def test_execution_time_validator(user):
    habit = Habit(
        user=user,
        place="Дома",
        time=timezone.now().time(),
        action="Долгое действие",
        execution_time=150  # > 120 секунд
    )
    with pytest.raises(ValidationError) as exc_info:
        habit.full_clean()
    assert "execution_time" in exc_info.value.message_dict


@pytest.mark.django_db
def test_pleasant_habit_cannot_have_reward(user, pleasant_habit):
    pleasant_habit.reward = "Шоколадка"
    with pytest.raises(ValidationError) as exc_info:
        pleasant_habit.full_clean()
    assert "reward" in exc_info.value.message_dict


@pytest.mark.django_db
def test_periodicity_validator(user):
    habit = Habit(
        user=user,
        place="Дома",
        time=timezone.now().time(),
        action="Редкая привычка",
        periodicity=10  # > 7 дней
    )
    with pytest.raises(ValidationError) as exc_info:
        habit.full_clean()
    assert "periodicity" in exc_info.value.message_dict


@pytest.mark.django_db
def test_cannot_link_non_pleasant_habit(user, habit):
    habit2 = Habit(
        user=user,
        place="Офис",
        time=timezone.now().time(),
        action="Сделать зарядку",
        execution_time=120,
        periodicity=1,
        associated_habit=habit  # habit не is_pleasant
    )
    with pytest.raises(ValidationError) as exc_info:
        habit2.full_clean()
    assert "associated_habit" in exc_info.value.message_dict