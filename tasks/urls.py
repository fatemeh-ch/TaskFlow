from django.urls import path, include
from tasks.views import TaskListView, TaskDetailView , ToggleSubTaskView

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='dashboard'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path("subtasks/<int:pk>/toggle/", ToggleSubTaskView.as_view(), name="toggle-subtask")
]
