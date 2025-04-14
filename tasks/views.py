from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskCreateSerializer, TaskSerializer

class TaskCreateAPIView(APIView):
    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            # Return the full task details using TaskSerializer
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from .models import User
from .serializers import TaskAssignmentSerializer

class TaskAssignAPIView(APIView):
    def post(self, request):
        serializer = TaskAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            task_id = serializer.validated_data['task_id']
            user_ids = serializer.validated_data['user_ids']
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

            # Retrieve users and add them to the task
            users = User.objects.filter(id__in=user_ids)
            if not users:
                return Response({'error': 'No valid users found'}, status=status.HTTP_404_NOT_FOUND)
            
            task.assigned_users.add(*users)
            task.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.generics import ListAPIView
from .serializers import TaskSerializer

class UserTasksListAPIView(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Task.objects.filter(assigned_users__id=user_id)

