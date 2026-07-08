from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
from django.utils import timezone

from tasks.choices import TaskStatus
from tasks.models import SubTask


def update_task_status(task):
    """
        Synchronize the status of a task with the state of its subtasks.

        If the task has at least one incomplete subtask, it is marked as
        pending and its completion timestamp is cleared. Otherwise, the task
        is marked as completed and the current time is recorded as its
        completion timestamp.
    """

    has_incomplete_subtasks=task.subtasks.filter(is_completed=False).exists()
    if has_incomplete_subtasks:
        task.status = TaskStatus.PENDING
        task.completed_at = None
    else:
        task.status = TaskStatus.COMPLETED
        task.completed_at = timezone.now()
    task.save(update_fields=['status', 'completed_at'])


@receiver(post_save, sender=SubTask)
def handle_subtask_saved(sender, instance, **kwargs):
    """
        Update the parent task whenever a subtask is created or modified.

        This signal ensures that the task status always reflects the current
        completion state of its subtasks after any subtask is saved.
    """
    update_task_status(instance.task)


@receiver(post_delete, sender=SubTask)
def handle_subtask_deleted(sender, instance, **kwargs):
    """
        Recalculate the parent task status after a subtask is deleted.

        Removing a subtask may change whether the parent task should remain
        pending or become completed, so the task state is synchronized after
        every deletion.
    """
    update_task_status(instance.task)