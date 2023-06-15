
from .takeone_project_use_case import TakeOneProjectUseCase
from .takeone_user_use_case import TakeOneUserUseCase
import musicspace_app.settings as app_settings

from musicspace_app.service_locator import takeone_client

class UseCaseFactory():

    def takeone_project_use_case(self) -> TakeOneProjectUseCase:
        return TakeOneProjectUseCase(
            takeone_client=takeone_client,
            profile_video_container_template_id=app_settings.TAKEONE_VIDEO_CONTAINER_TEMPLATE_ID
        )

    def takeone_user_use_case(self) -> TakeOneUserUseCase:
        return TakeOneUserUseCase(
            takeone_client=takeone_client,
            from_email=app_settings.FROM_EMAIL
        )

use_case_factory = UseCaseFactory()