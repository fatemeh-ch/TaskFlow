from django.db import models
from django.contrib.auth import get_user_model

from core.models import TimeStampedModel
from tasks.choices import TaskStatus, TaskPriority

# Create your models here.

User = get_user_model()


class Task(TimeStampedModel, models.Model):
    """
        Represents a task created by a user.

        Each task belongs to a single user and can be assigned
        to a category with a specific status, priority, and deadline.
    """

    class Meta:
        ordering = ["-created_at"]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_important = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=TaskStatus.choices, default=TaskStatus.PENDING)
    priority = models.CharField(
        max_length=20, choices=TaskPriority.choices, default=TaskPriority.MEDIUM)
    deadline = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, related_name='tasks')

    def __str__(self):
        return self.title


class Category(TimeStampedModel, models.Model):
    """
        Represents a task category used to organize tasks.

        Categories are shared across all users and contain
        a title, slug, and icon.
    """

    class Meta:
        ordering = ["title"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=150)

    def __str__(self):
        return self.title
