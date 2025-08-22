from django.contrib import admin
from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """Admin configuration for Record model."""
    list_display = ("id", "name", "value", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("id",)
