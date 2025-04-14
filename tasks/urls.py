from django.urls import path
from .views import TaskCreateAPIView, TaskAssignAPIView, UserTasksListAPIView

urlpatterns = [
    path('tasks/create/', TaskCreateAPIView.as_view(), name='task-create'),
    path('tasks/assign/', TaskAssignAPIView.as_view(), name='task-assign'),
    path('tasks/user/<int:user_id>/', UserTasksListAPIView.as_view(), name='user-tasks'),
]
