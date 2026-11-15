"""Turns SavedBook objects into JSON for the API (and back, for edits)."""

from rest_framework import serializers

from .models import SavedBook


class SavedBookSerializer(serializers.ModelSerializer):
    """The fields the API shows for one saved book.

    The owner (`user`) is never shown. Open Library facts and `created_at` are
    read-only; only `status`, `rating`, and `notes` can ever be changed.
    """

    class Meta:
        model = SavedBook
        fields = [
            "id",
            "work_key",
            "title",
            "author",
            "first_publish_year",
            "cover_id",
            "status",
            "rating",
            "notes",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "work_key",
            "title",
            "author",
            "first_publish_year",
            "cover_id",
            "created_at",
        ]
