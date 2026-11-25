from django.contrib import admin

from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ["action", "user", "time", "place", "is_pleasant", "is_public", "periodicity", "created_at"]
    list_filter = ["is_pleasant", "is_public", "periodicity"]
    search_fields = ["action", "place", "user__email"]
    readonly_fields = ["created_at"]
    autocomplete_fields = ["associated_habit"]