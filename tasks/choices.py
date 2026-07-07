from django.db import models


class TaskStatus(models.TextChoices):
    """
        Available status choices for a task.
    """

    PENDING = 'pending', 'در حال انجام'
    COMPLETED = 'completed', 'انجام شده'


class TaskPriority(models.TextChoices):
    """
        Available priority levels for a task.
    """
    
    LOW = 'low', 'کم'
    MEDIUM = 'medium', 'متوسط'
    HIGH = 'high', 'زیاد'
