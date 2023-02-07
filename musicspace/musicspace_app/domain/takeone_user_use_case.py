from musicspace_app.data import TakeOneClient
from musicspace_app.models import (
    Provider, TakeOneUser
)

class TakeOneUserUseCase:

    def __init__(
        self,
        takeone_client: TakeOneClient
    ):
        self.takeone_client = takeone_client

    def create_user(
        self,
        provider: Provider
    ) -> TakeOneUser:

        existing_takeone_user = provider.takeone_user
        if existing_takeone_user is not None:
            raise Exception("A TakeOne user already exists for this user.")

        request = TakeOneClient.CreateUserRequest(
            external_id=str(provider.id),
            display_name=provider.full_name,
            email_address=provider.user.email
        )

        ## issue request to create new user
        ## TODO - if this fails, check to see if the user already exists
        ## there is a constrait that external_id is unique to the org
        takeone_client_user = self.takeone_client.create_user(
            request=request
        )

        ## if the request was successful, save the takeone user object
        takeone_user = TakeOneUser(
            provider=provider,
            takeone_id=takeone_client_user.id
        )

        takeone_user.full_clean()
        takeone_user.save()

        return takeone_user



