from django.contrib import admin

from .models import SavedBook


@admin.register(SavedBook)
class SavedBookAdmin(admin.ModelAdmin):
    """Staff-only view of every user's saved books, for checking data while testing."""

    list_display = ["title", "user", "status", "rating", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["title", "author", "user__username"]
