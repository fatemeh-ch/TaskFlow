import jdatetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView

from tasks.models import Task, TaskStatus

# Create your views here.


class TaskListView(LoginRequiredMixin, ListView):
    """
        Display the authenticated user's dashboard.

        The dashboard shows only the current user's tasks along with
        aggregated statistics such as category counts, priority counts,
        pending tasks, completion progress, today's date, and the nearest
        upcoming task.
    """
        
    model = Task
    template_name = 'tasks/dashboard.html'
    context_object_name = 'tasks'
    paginate_by = 3

    def get_queryset(self):
        return (
            Task.objects.filter(user=self.request.user)
            .select_related('category')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = self.object_list


        # Today
        jdatetime.set_locale(jdatetime.FA_LOCALE)
        today = jdatetime.datetime.fromgregorian(datetime=timezone.now())
        context["today"] = today.strftime("%A %d %B %Y")

        # Categories
        context['category_counts'] = {
            'all': tasks.count(),
            'study': tasks.filter(category__slug='study').count(),
            'personal': tasks.filter(category__slug='personal').count(),
            'work': tasks.filter(category__slug='work').count(),
        }

        # Priorities
        context['priority_counts'] = {
            'high': tasks.filter(priority='high').count(),
            'medium': tasks.filter(priority='medium').count(),
            'low': tasks.filter(priority='low').count(),
        }

        # Pending Tasks
        context['pending_tasks'] = tasks.filter(
            status=TaskStatus.PENDING).count()

        # Progress
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status=TaskStatus.COMPLETED).count()

        context['total_tasks'] = total_tasks
        context['completed_tasks'] = completed_tasks
        context["progress"] = (
            round((completed_tasks / total_tasks) * 100) if total_tasks else 0)

        # Upcoming task
        context["upcoming_task"] = (
            tasks.filter(
                deadline__isnull=False,
                deadline__gte=timezone.now(),
            )
            .exclude(status=TaskStatus.COMPLETED)
            .order_by("deadline")
            .first()
        )

        return context
