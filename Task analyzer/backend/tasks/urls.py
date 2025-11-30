# backend/tasks/urls.py

from django.urls import path
from .views import task_list, analyze_tasks, suggest_tasks

urlpatterns = [
    path('tasks/', task_list, name='task_list'),          # GET/POST tasks
    path('tasks/analyze/', analyze_tasks, name='analyze_tasks'),  # POST analyze
    path('tasks/suggest/', suggest_tasks, name='suggest_tasks'),  # POST top 3 suggestions
]
