from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["owner"]
        
        
class CollaborateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["id","username","email"]