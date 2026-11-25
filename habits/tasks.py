import requests
from django.conf import settings
from django.utils import timezone
from celery import shared_task

from .models import Habit


@shared_task
def send_habit_reminders():
    """
    Периодическая задача: отправляет Telegram-уведомления о привычках,
    которые необходимо выполнить в текущую минуту.
    """
    now = timezone.now()

    # Получаем все привычки с заполненным telegram_chat_id
    habits = Habit.objects.select_related('user').exclude(user__telegram_chat_id__isnull=True)

    for habit in habits:
        # Проверяем, должен ли сегодня сработать триггер (кратно периодичности)
        days_since_creation = (now.date() - habit.created_at.date()).days
        if days_since_creation % habit.periodicity == 0:
            # Проверяем совпадение времени (часы и минуты)
            if now.hour == habit.time.hour and now.minute == habit.time.minute:
                message = (
                    f"🔔 <b>Напоминание о привычке!</b>\n\n"
                    f"📍 <b>Место:</b> {habit.place}\n"
                    f"⏰ <b>Время:</b> {habit.time.strftime('%H:%M')}\n"
                    f"🎯 <b>Действие:</b> {habit.action}\n"
                    f"⏱️ <b>Время на выполнение:</b> {habit.execution_time} сек."
                )

                if habit.is_pleasant:
                    message += "\n\n🌟 Это приятная привычка для вознаграждения!"
                elif habit.reward:
                    message += f"\n\n🎁 <b>Вознаграждение:</b> {habit.reward}"

                url = f"{settings.TELEGRAM_API_URL}/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

                try:
                    response = requests.post(
                        url,
                        json={
                            "chat_id": habit.user.telegram_chat_id,
                            "text": message,
                            "parse_mode": "HTML"
                        },
                        timeout=5
                    )
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    # Логируем ошибку, но не прерываем выполнение для других привычек
                    print(f"Ошибка отправки уведомления для привычки {habit.id}: {e}")