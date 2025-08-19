from rest_framework import permissions
from .models import Project
class IsProjectMember(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):

        project = None
        if isinstance(obj, Project):
            project = obj
        elif hasattr(obj, 'project'):
            project = obj.project
        elif hasattr(obj, 'task'):
            project = obj.task.project
        else :
            return False
        

        return request.user in project.member.all()