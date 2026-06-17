from django.db import models
from projects.models import Project
import uuid 

# Create your models here.
class Diagram(models.Model):
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="diagram"
    )
    
    diagram_data = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Diagram - {self.project.name}"
    
    
class SharedDiagram(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    share_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)