from django.urls import path
from . import views

urlpatterns = [
    path('' , views.projects , name="projects"),
    path('<str:pk>' , views.projectPK , name='projectPK'),
    path('create_project/' , views.create_project , name="create-project"),
    path('update_project/<str:pk>/' , views.update_project , name="update-project"),
    path('delete_project/<str:pk>/' , views.delete_project , name="delete-project"),
]
