import jdatetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView

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
        """
            Return the authenticated user's tasks, optionally filtered by a query parameter.

            Supported filters:
                - all: Return all tasks (default behavior).
                - important: Tasks marked as important.
                - incomplete: Tasks with pending status.
                - overdue: Pending tasks whose deadline has already passed.
                - today: Tasks scheduled for today.

            Search:
                - search: Filter tasks by title using a case-insensitive lookup.

            The related category is fetched using `select_related()` to reduce
            database queries when rendering the dashboard.
        """

        today = timezone.localdate()

        queryset = Task.objects.filter(
            user=self.request.user).select_related('category')
        filter_name = self.request.GET.get('filter')

        if filter_name == 'important':
            queryset = queryset.filter(is_important=True)

        elif filter_name == 'incomplete':
            queryset = queryset.filter(status=TaskStatus.PENDING)

        elif filter_name == 'overdue':
            queryset = queryset.filter(
                deadline__lt=timezone.now(), status=TaskStatus.PENDING)

        elif filter_name == 'today':
            queryset = queryset.filter(deadline__date=today)

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add dashboard-specific context data for rendering the task overview.

        In addition to the paginated task list provided by ``ListView``, this
        method injects summary statistics and helper values used throughout the
        dashboard template, including:

        - Current date in the Jalali calendar.
        - Task counts grouped by category.
        - Task counts grouped by priority.
        - Number of pending tasks.
        - Total and completed task counts.
        - Overall completion progress percentage.
        - The nearest upcoming pending task.

        Returns:
            dict: Context data required to render the dashboard template.
    """

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


class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    Display the details of a single task belonging to the authenticated user.

    This view ensures that users can only access their own tasks by
    restricting the queryset to tasks created by the current user.
    Additional context data is provided for rendering Jalali-formatted
    creation and update dates in the template.
    """

    model = Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"

    def get_object(self, queryset=None):
        """
        Retrieve the requested task while enforcing object-level ownership.

        Only tasks that belong to the authenticated user can be accessed.
        Attempting to access another user's task will result in a 404 error.
        """
        queryset = Task.objects.filter(user=self.request.user)
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        """
        Add extra context required by the task detail template.

        The task's creation and last update timestamps are converted to
        Jalali format for display in the sidebar.
        """
        context = super().get_context_data(**kwargs)

        jdatetime.set_locale(jdatetime.FA_LOCALE)

        created_at = jdatetime.datetime.fromgregorian(
            datetime=self.object.created_at
        )
        updated_at = jdatetime.datetime.fromgregorian(
            datetime=self.object.updated_at
        )

        context["created_at"] = created_at.strftime("%d %B")
        context["updated_at"] = updated_at.strftime("%d %B")

        return context
