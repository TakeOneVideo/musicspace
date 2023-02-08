from musicspace_app.data import TakeOneClient
from musicspace_app.models import (
    TakeOneUser, TakeOneProject
)

class TakeOneProjectUseCase:

    def __init__(
        self,
        takeone_client: TakeOneClient
    ):
        self.takeone_client = takeone_client

    def create_project(
        self,
        takeone_user: TakeOneUser
    ) -> TakeOneProject:

        display_name = f"{takeone_user.provider.full_name}'s project"
        request = TakeOneClient.CreateProjectRequest(
            user=takeone_user.takeone_id,
            display_name=display_name
        )

        takeone_client_project = self.takeone_client.create_project(
            request=request
        )

        project = TakeOneProject(
            id=takeone_client_project.id,
            takeone_user=takeone_user,
            status=takeone_client_project.state,
            published=takeone_client_project.publishing_status == 'published',
            show_video=takeone_client_project.publishing_status == 'published'
        )

        project.full_clean()
        project.save()

        return project

    def handle_project_notification(
        self,
        project_data: dict
    ):
        takeone_client_project = TakeOneClient.Project(**project_data)

        ## update local model
        TakeOneProject.objects.filter(
            id=takeone_client_project.id
        ).update(
            status=takeone_client_project.state,
            published=takeone_client_project.publishing_status == 'published',
            show_video=takeone_client_project.publishing_status == 'published'
        )

