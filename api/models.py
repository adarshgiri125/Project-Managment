from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length = 20)
    description = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add= True)
    member = models.ManyToManyField(User,related_name='projects')
    owner = models.ForeignKey(User, related_name='owned_projcts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=20, unique = True)

    def __str__(self):
        return self.name

class Task(models.Model):

    class Status(models.TextChoices):
        TODO = 'TODO', 'To Do'
        IN_PROGRESS = 'IN_PROGESS', 'In Progress'
        DONE = 'DONE', 'Done'

    
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    priority = models.IntegerField(default=0)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User,related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag,related_name='tasks', blank = True)
    status = models.CharField(max_length=20,choices=Status.choices, default=Status.TODO)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.CharField(max_length=40)
    task = models.ForeignKey(Task,related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.author} on {self.task}"