from django.shortcuts import render
from .serializers import ProjectSerializer,CollaborateSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Project, ProjectCollaborator
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.db.models import Q
from .utils import get_project_for_user

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user)
            |
            Q(collaborators__user=self.request.user)
        ).distinct()
        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user)
            |
            Q(collaborators__user=self.request.user)
        ).distinct()
    
    
    
class InviteCollaboratorView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request, project_id):
        project = Project.objects.get(id=project_id, owner = request.user)
        email = request.data.get("email")
        user = User.objects.get(email=email)
        ProjectCollaborator.objects.get_or_create(project = project, user= user)

        return Response({"message":"Collaborator Added"})
    
    
class CollaboratorListView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, project_id):
        project = get_project_for_user(
            project_id,
            request.user
        )
        collaborators = [item.user for item in project.collaborators.all() ] 
        serializer = CollaborateSerializer(collaborators, many=True)

        return Response(serializer.data)


class RemoveCollaboratorView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self, request, project_id, user_id):
        project = Project.objects.get(id=project_id, owner=request.user)
        ProjectCollaborator.objects.filter(project=project, user_id=user_id).delete()

        return Response({"message":"Removed"})