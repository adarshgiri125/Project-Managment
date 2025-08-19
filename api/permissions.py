from rest_framework import permissions

class IsProjectMember(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return self.request.user == obj.members.all()