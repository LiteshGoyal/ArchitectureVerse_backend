from django.db import models
from projects.models import Project


class ChatSession(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role= models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ArchitectureReview(models.Model):
    project= models.ForeignKey(Project, on_delete=models.CASCADE, related_name="reviews")
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)