from django.shortcuts import render
from rest_framework import viewsets, permissions

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
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        task_pk = self.kwargs['task-pk']
        return Comment.objects.filter(task_id = task_pk)
    
    
    def perform_create(self, serializer):
        task_pk = self.kwargs['task-pk']
        serializer.save(author = self.request.user,task_id = task_pk)
    
class TaskViewSet(viewsets.ModelViewSet):
    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # def perform_create(self, serializer):
    #     serializer.save(assignee = self.request.user)
    def get_queryset(self):
        project_pk = self.kwargs['project-pk']
        
        return Task.object.filter(project_id = project_pk)
    
    def perform_create(self, serializer):
        project_pk = self.kwargs['project-pk']
        serializer.save(project_id = project_pk)
    
    
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]