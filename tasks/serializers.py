from rest_framework import serializers
from .models import Task, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile']

class TaskSerializer(serializers.ModelSerializer):
    # Serialize the user details for assigned users
    assigned_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'task_type',
            'completed_at',
            'status',
            'assigned_users'
        ]

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name', 'description']  # Add extra fields if needed


class TaskAssignmentSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        allow_empty=False,
        help_text="List of user IDs to assign the task to."
    )
