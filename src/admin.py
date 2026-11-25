from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("action", "user", "time", "place", "is_pleasant", "is_public", "created_at")
    list_filter = ("is_pleasant", "is_public", "time")
    search_fields = ("action", "place", "user__email")
    readonly_fields = ("created_at",)
