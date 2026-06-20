from google import genai
from decouple import config
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from uuid import uuid4

from projects.models import Project
from .models import (ChatMessage,ChatSession, ArchitectureReview)
from .serializers import ChatMessageSerializer, ArchitectureReviewSerializer
from projects.utils import (get_project_for_user)

class ReviewArchitectureView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        documentation = request.data.get("documentation")
        
        client = genai.Client(api_key=config("GEMINI_API_KEY"))
        
        prompt = f""" You are a software architect. 
        Review the following architecture and provide:
        1. Strengths
        2. Weaknesses
        3. Suggestions
        
        Architecture:
        {documentation}
        """
        
        response = (client.models.generate_content(model="gemini-2.5-flash",contents=prompt,))
        project = get_project_for_user(request.data.get("project_id"),request.user)
        
        ArchitectureReview.objects.create(project=project, content=response.text)
        
        return Response({
            "review": response.text
        })
        
        
class GenerateArchitectureView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        prompt = request.data.get("prompt")
        client = genai.Client(api_key = config("GEMINI_API_KEY"))
        
        architecture_prompt=f"""
        Generate a software declaration architecture.
        
        User Request:{prompt}
        Return ONLY valid JSON.
        
        Format:

        {{
          "nodes":[
            {{
              "id":"1",
              "label":"React"
            }}
          ],

          "edges":[
            {{
              "source":"1",
              "target":"2"
            }}
          ]
        }}

        No markdown.
        No explanation.
        Only JSON.
        """
        
        response = (client.models.generate_content(model="gemini-2.5-flash",contents=architecture_prompt))
        
        
        
        return Response({
            "architecture":response.text
        })
        

class ExplainArchitectureView(APIView):
  permission_classes=[IsAuthenticated]
  
  def post(self, request):
    documentation = request.data.get("documentation")
    
    client = genai.Client(api_key=config("GEMINI_API_KEY"))
    
    prompt = f"""
    Explain this software Architecture in simple language. 
    
    Explain:
    1. Purpose of each component
    2. Data flow
    3. Overall architecture
    
    Architecture:
    {documentation}
    """
    
    response = (client.models.generate_content(model="gemini-2.5-flash",contents=prompt,))
    
    return Response({"explanation":response.text})
  
  
class ArchitectureChatView(APIView):
  permission_classes = [IsAuthenticated]
  
  def post(self,request):
    documentation = request.data.get("documentation")
    
    question = request.data.get("question")
    
    client = genai.Client(api_key = config("GEMINI_API_KEY"))
    prompt = f"""
    YOu are a software architecture expert.
    
    Architecture:
    {documentation}
    
    User Question:
    {question}
    
    Answer specifically based on the provided architecture and dont keep the answer too long.
    """
    
    project = get_project_for_user(request.data.get("project_id"),request.user)
    
    session, _ = (ChatSession.objects.get_or_create(project=project))
    
    response = (client.models.generate_content(model="gemini-2.5-flash",contents=prompt))
    
    ChatMessage.objects.create(session=session, role="user", content=question)
    
    ChatMessage.objects.create(session=session, role="assistant", content=response.text)
    
    
    
    return Response({"answer":response.text})
  
  
  
class ChatHistoryView(APIView):
  permission_classes=[IsAuthenticated]
  
  def get(self, request, project_id):
    project = get_project_for_user(project_id,request.user)
    
    session = (ChatSession.objects.filter(project=project).first())
    
    if not session:
      return Response([])
    messages = (session.messages.all().order_by("created_at"))
    
    serializer = (ChatMessageSerializer(messages, many=True))
    return Response(
            serializer.data
        )
    
    
class ImproveArchitectureView(APIView):
  permission_classes=[IsAuthenticated]
  
  def post(self, request):
    documentation = request.data.get("documentation")
    
    client = genai.Client(api_key=config("GEMINI_API_KEY"))
    
    prompt = f"""
    Analyze the software architecture.
    {documentation}
    
    Suggest Improvements. 
    Return ONLY JSON. 
    Format:
    {{
      "suggestions":[
        {{
          "label":"Redis",
          "reason":"Cache database queries" ,
          "connect_to":[
            "Django"
          ]
        }}
      ]
    }}
    No markdown. 
    No explanation. 
    Only JSON. 
    """
    response = (client.models.generate_content(model="gemini-2.5-flash",contents=prompt))
    
    return Response({"suggestions":response.text})
  
  
  
class ReviewHistoryView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        project_id
    ):

        project = get_project_for_user(project_id,request.user)

        reviews = (
            project.reviews
            .all()
            .order_by(
                "-created_at"
            )
        )

        serializer = (
            ArchitectureReviewSerializer(
                reviews,
                many=True
            )
        )

        return Response(
            serializer.data
        )