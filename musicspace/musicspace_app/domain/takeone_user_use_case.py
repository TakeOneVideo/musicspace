from typing import Optional
from django.core import mail
from django.template.loader import render_to_string

from musicspace_app.data import TakeOneClient, CreateUserRequest
from musicspace_app.models import (
    Provider, TakeOneUser
)

class TakeOneUserUseCase:

    def __init__(
        self,
        takeone_client: TakeOneClient,
        from_email: str
    ):
        self.takeone_client = takeone_client
        self.from_email = from_email

    def create_user(
        self,
        provider: Provider
    ) -> TakeOneUser:

        existing_takeone_user = provider.takeone_user
        if existing_takeone_user is not None:
            raise Exception("A TakeOne user already exists for this user.")

        request = CreateUserRequest(
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

    def get_auth_code(
        self,
        user: TakeOneUser
    ) -> str:
        return self.takeone_client.authorize(
            user_id=user.takeone_id
        )
    
    def _generate_invitation_email(
        self,
        takeone_user: TakeOneUser
    ) -> mail.EmailMessage:

        recipient_description = takeone_user.provider.full_name
        code = self.get_auth_code(user=takeone_user)

        subject = f'Your TakeOne Video Invitation'
        context = {
            'recipient_description': recipient_description,
            'code': code
        }

        invitation_html_email = render_to_string(
            'musicspace_app/emails/invitation_email.html',
            context=context
        )

        invitation_text_email = render_to_string(
            'musicspace_app/emails/invitation_email.txt',
            context=context
        )

        msg = mail.EmailMultiAlternatives(
            subject=subject,
            body=invitation_text_email,
            from_email=self.from_email,
            to=[takeone_user.provider.user.email]
        )

        msg.attach_alternative(invitation_html_email, "text/html")

        return msg
    
    def send_invitation_email(
        self,
        takeone_user: TakeOneUser
    ):
        connection = mail.get_connection()
        email_message = self._generate_invitation_email(
            takeone_user=takeone_user
        )
        connection.send_messages([email_message])