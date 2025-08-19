from rest_framework import serializers
from .models import Tag , Task, Comment, Project
from django.contrib.auth.models import User
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
  

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source = 'author.username')
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'task', 'author', 'author_username', 'created_at']
        read_only_fields = ['author', 'task']      

class TaskSerializer(serializers.ModelSerializer):
    
    asignee_username = serializers.ReadOnlyField(source = 'assignee.username', allow_null = True)
    
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset = Tag.objects.all())
    class Meta:
        model = Task
        fiels = ['id','title', 'description', 'status', 'priority', 'project', 'assignee', 'assignee_username', 'tags', 'created_at', 'updated_at' ]
        
class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    member = UserSerializer(many=True,read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'members', 'created_at']
    
    
    
        
