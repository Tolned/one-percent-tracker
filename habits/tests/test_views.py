import pytest
from rest_framework import status
from habits.models import Habit
from django.utils import timezone


@pytest.mark.django_db
class TestHabitViewSet:
    def test_list_habits_pagination(self, authenticated_client, user):
        # Создаем 6 привычек, чтобы проверить пагинацию (PAGE_SIZE=5)
        for i in range(6):
            Habit.objects.create(
                user=user,
                place=f"Место {i}",
                time=timezone.now().time(),
                action=f"Действие {i}",
                execution_time=60
            )

        response = authenticated_client.get("/api/habits/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 5  # Пагинация по 5
        assert response.data["count"] == 6

    def test_create_habit(self, authenticated_client):
        data = {
            "place": "Спортзал",
            "time": "08:00:00",
            "action": "Пробежка",
            "execution_time": 120,
            "periodicity": 1
        }
        response = authenticated_client.post("/api/habits/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Habit.objects.count() == 1
        assert Habit.objects.first().user.email == "test@example.com"

    def test_cannot_update_others_habit(self, authenticated_client, user):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        other_user = User.objects.create_user(email="other@example.com", password="pass")
        other_habit = Habit.objects.create(
            user=other_user,
            place="Дома",
            time=timezone.now().time(),
            action="Чтение",
            execution_time=30
        )

        response = authenticated_client.patch(f"/api/habits/{other_habit.id}/", {"action": "Новое"})
        assert response.status_code == status.HTTP_404_NOT_FOUND  # IsOwnerOrReadOnly скрывает чужие


@pytest.mark.django_db
class TestPublicHabitViewSet:
    def test_list_public_habits(self, api_client, user):
        Habit.objects.create(
            user=user,
            place="Парк",
            time=timezone.now().time(),
            action="Прогулка",
            execution_time=60,
            is_public=True
        )
        Habit.objects.create(
            user=user,
            place="Дома",
            time=timezone.now().time(),
            action="Сон",
            execution_time=480,
            # Ошибка валидации, но для теста публичности создадим вручную через manager или исправим
            is_public=False
        )
        # Исправим время на валидное для второго, чтобы он создался
        h2 = Habit(user=user, place="Дома", time=timezone.now().time(), action="Сон", execution_time=60,
                   is_public=False)
        h2.save()

        response = api_client.get("/api/public-habits/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["action"] == "Прогулка"