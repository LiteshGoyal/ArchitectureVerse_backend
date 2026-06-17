from rest_framework import serializers

from .models import ChatMessage, ArchitectureReview

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ChatMessage
        fields="__all__"
        
        
class ArchitectureReviewSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = ArchitectureReview
        fields = "__all__"