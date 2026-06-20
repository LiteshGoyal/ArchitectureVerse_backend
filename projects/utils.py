from projects.models import (Project, ProjectCollaborator)

from rest_framework.exceptions import PermissionDenied

def get_project_for_user(project_id, user):
    project = Project.objects.get(id=project_id)
    is_owner = (project.owner==user)

    is_collaborator=(ProjectCollaborator.objects.filter(project=project, user=user).exists())

    if not(is_owner or is_collaborator):
        raise PermissionDenied("You do not have access to this project")

    return project