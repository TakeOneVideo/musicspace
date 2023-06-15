from typing import Dict, Any, Optional
from django.core import mail
from django.template.loader import render_to_string
from musicspace_app.data import (
    TakeOneClient, TakeOneWebhookRequest, CreateVideoContainerRequest,
    CreateProjectRequest
)
from musicspace_app.models import (
    TakeOneUser, TakeOneProfileVideoContainer
)
import musicspace_app.errors as app_errors

class TakeOneProjectUseCase:

    def __init__(
        self,
        takeone_client: TakeOneClient,
        profile_video_container_template_id: str
    ):
        self.takeone_client = takeone_client
        self.profile_video_container_template_id = profile_video_container_template_id

    def create_profile_video_container(
        self,
        takeone_user: TakeOneUser
    ) -> TakeOneProfileVideoContainer:
        
        display_name = f"{takeone_user.provider.full_name}'s profile video"

        ## create video container
        request = CreateVideoContainerRequest(
            template=self.profile_video_container_template_id,
            name=display_name
        )

        takeone_client_video_container = self.takeone_client.create_video_container(
            request=request
        )

        video_container = TakeOneProfileVideoContainer(
            id=takeone_client_video_container.id,
            template=self.profile_video_container_template_id,
            takeone_user=takeone_user
        )

        video_container.full_clean()
        video_container.save()

        return video_container

    def create_project(
        self,
        takeone_user: TakeOneUser,
        video_container: TakeOneProfileVideoContainer
    ):

        display_name = f"{takeone_user.provider.full_name}'s project"
        request = CreateProjectRequest(
            user=takeone_user.takeone_id,
            video_container=video_container.id,
            organization_display_name=display_name
        )

        takeone_client_project = self.takeone_client.create_project(
            request=request
        )

    def decode_webhook_request(
        self,
        webhook_request_dict: Dict[str, Any]
    ) -> TakeOneWebhookRequest:
        try:
            return TakeOneWebhookRequest(**webhook_request_dict)
        except BaseException as e:
            print(f'an exception occurred parsing the webhook request: {e}')
            raise app_errors.BadRequestError()

    def handle_webhook(
        self,
        webhook_request: TakeOneWebhookRequest
    ):
        
        ## update local video container with the streaming video info
        video_container = TakeOneProfileVideoContainer.objects.get(
            id=webhook_request.video_container.id
        )

        video_stream = webhook_request.video_container.video_stream
        if video_stream:
            video_container.video_stream_src = video_stream.src
            video_container.video_stream_type = video_stream.type
            video_container.video_stream_video_format = video_stream.video_format
        else:
            video_container.video_stream_src = ''
            video_container.video_stream_type = ''
            video_container.video_stream_video_format = ''

        video_container.full_clean()
        video_container.save()

    def update_video_container_from_server(
        self,
        video_container: TakeOneProfileVideoContainer
    ) -> TakeOneProfileVideoContainer:
        
        takeone_client_video_container = self.takeone_client.fetch_video_container(
            video_container_id=video_container.id
        )

        video_stream = takeone_client_video_container.video_stream
        if video_stream:
            video_container.video_stream_src = video_stream.src
            video_container.video_stream_type = video_stream.type
            video_container.video_stream_video_format = video_stream.video_format
        else:
            video_container.video_stream_src = ''
            video_container.video_stream_type = ''
            video_container.video_stream_video_format = ''

        video_container.full_clean()
        video_container.save()

        return video_container