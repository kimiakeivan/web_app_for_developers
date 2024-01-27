from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer 
from project.models import project 



@api_view(['GET'])
def getRoutes(request) : 
    return Response(None)

@api_view(['GET'])
def getProjects(request) : 
    return Response(None)