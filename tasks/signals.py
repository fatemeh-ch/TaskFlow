from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from tasks.choices import TaskStatus
from tasks.models import SubTask


@receiver(post_save, sender=SubTask)
def change_task_status(sender, instance, **kwargs):
    """
        Update the parent task status whenever one of its subtasks changes.

        If all subtasks are completed, the task is marked as completed and
        the completion timestamp is recorded. Otherwise, the task is marked
        as pending and its completion timestamp is cleared.
    """

    task = instance.task

    has_incomplete_subtasks = task.subtasks.filter(
        is_completed=False
    ).exists()

    if has_incomplete_subtasks:
        task.status = TaskStatus.PENDING
        task.completed_at = None
    else:
        task.status = TaskStatus.COMPLETED
        task.completed_at = timezone.now()

    task.save()
