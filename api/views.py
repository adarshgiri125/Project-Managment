from django.shortcuts import render
from rest_framework import viewsets, permissions

from .tasks import send_assignment_notification

from .serializers import ProjectSerializer, CommentSerializer, TaskSerializer, TagSerializer
from .models import Comment, Task, Tag

from .permissions import IsProjectMember

# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]
    
    def get_queryset(self):
        return self.request.user.projects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        project = serializer.save(owner = self.request.user)
        project.member.add(self.request.user)
        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]
    
    def get_queryset(self):
        task_pk = self.kwargs['task_pk']
        return Comment.objects.filter(task_id = task_pk)
    
    
    def perform_create(self, serializer):
        task_pk = self.kwargs['task_pk']
        serializer.save(author = self.request.user,task_id = task_pk)
    
class TaskViewSet(viewsets.ModelViewSet):
    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]

    def perform_update(self, serializer):
        original_assignee = serializer.instance.assignee

        updated_task = serializer.save()

        if updated_task.assignee != original_assignee and updated_task.assignee is not None:
            print(f"Task {updated_task.id} was assigned to {updated_task.assignee.username}. Firing notification task...")
            # Trigger the background task!
            send_assignment_notification.delay(
                task_id=updated_task.id,
                assigned_by_user_id=self.request.user.id,
                assignee_id=updated_task.assignee.id
            )
    
    # def perform_create(self, serializer):
    #     serializer.save(assignee = self.request.user)
    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        
        return Task.objects.filter(project_id = project_pk)
    
    def perform_create(self, serializer):
        project_pk = self.kwargs['project_pk']
        serializer.save(project_id = project_pk)

    
    
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]