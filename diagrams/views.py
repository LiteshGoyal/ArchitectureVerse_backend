from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from projects.models import Project
from .models import Diagram, SharedDiagram

class DiagramView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id, owner=request.user)
        
        diagram, created = Diagram.objects.get_or_create(
            project=project,
            defaults={
                "diagram_data":{
                    "nodes":[],
                    "edges":[]
                }
            }
        )
        
        return Response(
            diagram.diagram_data
        )
        
    def put(self, request, project_id):
        project = Project.objects.get(id=project_id, owner = request.user)
        
        diagram, created = Diagram.objects.get_or_create(project=project)
        
        diagram.diagram_data = request.data 
        diagram.save()
        
        return Response({
            "message":"Diagram saved successfully"
        })
        
        
class ShareDiagramView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request, project_id):
        project = Project.objects.get(id=project_id, owner = request.user)
        share, _ = ( SharedDiagram.objects.get_or_create(project=project))
        
        return Response({"share_id":str(share.share_id)})
    
    
class PublicDiagramView(APIView):
    permission_classes=[]
    def get(self, request, share_id):
        shared = SharedDiagram.objects.get(share_id=share_id)
        diagram = Diagram.objects.get(project=shared.project)

        return Response(diagram.diagram_data)