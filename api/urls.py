from rest_framework_nested import routers
from . import views
from django.urls import path, include

router = routers.DefaultRouter()

router.register(r'projects',views.ProjectViewSet ,basename='project')
router.register(r'tags', views.TagViewSet, basename='tag')


project_router = routers.NestedSimpleRouter(router, r'projects', lookup = 'project')
project_router.register(r'tasks', views.TaskViewSet, basename='project-task')

task_router = routers.NestedSimpleRouter(project_router, r'tasks', lookup = 'task')
task_router.register(r'comments', views.CommentViewSet, basename='task-comment')

urlpatterns = [
    path('',include(router.urls)),
    path('', include(project_router.urls)),
    path('',include(task_router.urls)),
]
 