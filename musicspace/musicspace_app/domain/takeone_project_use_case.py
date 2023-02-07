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
            takeone_user=takeone_user,
            status=takeone_client_project.state,
            published=takeone_client_project.publishing_status == 'published',
            show_video=False
        )

        project.full_clean()
        project.save()

        return project