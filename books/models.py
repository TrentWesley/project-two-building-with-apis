from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class SavedBook(models.Model):
    """One book that one user saved to their reading list."""

    class Status(models.TextChoices):
        WANT_TO_READ = "want_to_read", "Want to Read"
        READING = "reading", "Reading"
        FINISHED = "finished", "Finished"

    # Owner: deleting a user also deletes their saved books.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_books")

    # Facts from Open Library (read-only after saving).
    work_key = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    first_publish_year = models.IntegerField(null=True, blank=True)
    cover_id = models.IntegerField(null=True, blank=True)

    # The user's own information (editable).
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.WANT_TO_READ
    )
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # A user can save each Open Library work only once.
            models.UniqueConstraint(
                fields=["user", "work_key"], name="unique_work_per_user"
            ),
        ]

    def __str__(self):
        return self.title
