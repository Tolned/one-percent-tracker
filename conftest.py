import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from habits.models import Habit
from django.utils import timezone

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="test@example.com",
        password="strongpassword123",
        telegram_chat_id="123456789"
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def habit(user):
    return Habit.objects.create(
        user=user,
        place="Дома",
        time=timezone.now().replace(hour=10, minute=0, second=0, microsecond=0).time(),
        action="Выпить стакан воды",
        execution_time=60,
        periodicity=1,
        is_public=False
    )


@pytest.fixture
def pleasant_habit(user):
    return Habit.objects.create(
        user=user,
        place="Ванная",
        time=timezone.now().replace(hour=20, minute=0, second=0, microsecond=0).time(),
        action="Принять ванну с пеной",
        is_pleasant=True,
        execution_time=120,
        periodicity=1,
        is_public=False
    )