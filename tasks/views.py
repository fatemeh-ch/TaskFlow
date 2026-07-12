from django.shortcuts import render
from django.views.generic.list import ListView

from tasks.models import Task

# Create your views here.

class TaskListView(ListView):
    model=Task
    template_name='tasks/dashboard.html'