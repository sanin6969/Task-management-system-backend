from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    STATUS_CHOICES = [
        ("accepted", "Accepted"),
        ("pending", "Pending"),
        ("work_in_progress", "Work in Progress"),
        ("completed", "Completed"),
        ("declined", "Declined"),
        ("not_completed", "Not Completed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=False, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    users = models.ManyToManyField(User, related_name="assigned_tasks")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def check_overdue(self):
        if (
            self.due_date
            and self.status not in ["completed", "declined", "not_completed"]
            and timezone.now() > self.due_date
        ):
            self.status = "not_completed"
            self.save()
