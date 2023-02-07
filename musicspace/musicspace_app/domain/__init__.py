
from .takeone_project_use_case import TakeOneProjectUseCase
from .takeone_user_use_case import TakeOneUserUseCase

from musicspace_app.service_locator import takeone_client

class UseCaseFactory():

    def takeone_project_use_case(self) -> TakeOneProjectUseCase:
        return TakeOneProjectUseCase(
            takeone_client=takeone_client
        )

    def takeone_user_use_case(self) -> TakeOneUserUseCase:
        return TakeOneUserUseCase(
            takeone_client=takeone_client
        )

use_case_factory = UseCaseFactory()