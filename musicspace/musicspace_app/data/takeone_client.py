from typing import Optional, List
from datetime import datetime
import httpx
from pydantic import BaseModel

class TakeOneProjectLite(BaseModel):
    id: str
    display_name: Optional[str]
    created_date_time: datetime
    modified_date_time: datetime

class TakeOneClient:

    class User(BaseModel):
        id: str
        external_id: Optional[str]
        display_name: Optional[str]
        email_address: Optional[str]
        projects: List[TakeOneProjectLite]

    class Project(TakeOneProjectLite):
        user: str
        state: str
        publishing_status: str
        hotlinking_protection_enabled: bool
        allowed_origins: List[str]
        internal_project_id: str

    class CreateUserRequest(BaseModel):
        external_id: Optional[str]
        display_name: Optional[str]
        email_address: Optional[str]

    class CreateProjectRequest(BaseModel):
        user: str
        display_name: Optional[str]
        # hotlinking_protection_enabled: bool = False
        # allowed_origins: List[str]

    class AuthorizationCodeRequest(BaseModel):
        user: str

    class AuthorizationCodeResponse(BaseModel):
        code: str

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str
    ):
        self.base_url = base_url
        self.auth = (client_id, client_secret)

    def create_user(
        self,
        request: CreateUserRequest
    ) -> User:

        url = f'{self.base_url}/users'
        r = httpx.post(
            url, 
            json=request.dict(),
            auth=self.auth, 
            timeout=30
        )

        if r.status_code >= 400:
            response_body = r.json()
            print(response_body)

        r.raise_for_status()
        response_body = r.json()
        return self.User(**response_body)

    def create_project(
        self,
        request: CreateProjectRequest
    ) -> Project:

        url = f'{self.base_url}/projects'
        r = httpx.post(
            url, 
            json=request.dict(),
            auth=self.auth, 
            timeout=30
        )

        if r.status_code == 400:
            response_body = r.json()
            print(response_body)

        r.raise_for_status()
        response_body = r.json()
        return self.Project(**response_body)

    def authorize(
        self,
        user_id: str
    ) -> str:

        request = self.AuthorizationCodeRequest(
            user=user_id
        )

        url = f'{self.base_url}/authorize'
        r = httpx.post(
            url, 
            json=request.dict(),
            auth=self.auth, 
            timeout=30
        )

        if r.status_code == 400:
            response_body = r.json()
            print(response_body)

        r.raise_for_status()
        response_body = r.json()
        auth_code_response = self.AuthorizationCodeResponse(**response_body)
        return auth_code_response.code

