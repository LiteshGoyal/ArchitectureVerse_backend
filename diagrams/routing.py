from django.urls import re_path

from .consumers import DiagramConsumer

websocket_urlpatterns=[
    re_path(r"ws/diagram/(?P<project_id>\d+)/$",
            DiagramConsumer.as_asgi(),
    )

]