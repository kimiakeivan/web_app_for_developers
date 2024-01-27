from rest_framework import serializers
from project.models import project

class ProjectSerializer(serializers.ModelSerializer) : 
    class Meta : 
        model = project 
        fields = '__all__'