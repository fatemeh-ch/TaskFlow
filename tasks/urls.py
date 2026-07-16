from django.urls import path, include
from tasks.views import TaskListView

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='dashboard')
]
