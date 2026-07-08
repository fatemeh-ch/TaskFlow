from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

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
        'Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if self.status == TaskStatus.COMPLETED:
            self.completed_at = timezone.now()
        else:
            self.completed_at = None
        super().save(*args, **kwargs)


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


class SubTask(TimeStampedModel, models.Model):
    """
        Represents a single checklist item belonging to a task.
    """

    title = models.CharField(max_length=250)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='subtasks')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order', 'created_at')
        verbose_name = "Sub Task"
        verbose_name_plural = "Sub Tasks"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_completed:
            self.completed_at = timezone.now()
        else:
            self.completed_at = None

        super().save(*args, **kwargs)
