from typing import Optional, List
from datetime import datetime
import httpx
from pydantic import BaseModel
from uuid import UUID

from enum import Enum

class TakeOneProjectLite(BaseModel):
    id: str
    organization_display_name: Optional[str]
    created_date_time: datetime
    modified_date_time: datetime

class User(BaseModel):
    id: str
    external_id: Optional[str]
    display_name: Optional[str]
    email_address: Optional[str]
    projects: List[TakeOneProjectLite]

class VideoFormat(str, Enum):
    LANDSCAPE = 'landscape'
    PORTRAIT = 'portrait'
    SQUARE = 'square'

class RecordingOrientation(str, Enum):
    LANDSCAPE = 'landscape'
    SQUARE = 'square'

class VideoContainerType(str, Enum):
    SINGLE = 'single'
    SUBSCRIPTION = 'subscription'

class FeatureInclusion(str, Enum):
    YES = 'yes'
    NO = 'no'
    DEFER_TO_USER = 'defer_to_user'

class VideoContainerTemplate(BaseModel):
    id: str
    container_type: VideoContainerType
    name: str
    description: Optional[str]
    video_hosting_enabled: bool
    manager_review_required: bool
    video_format: VideoFormat
    recording_video_orientation: RecordingOrientation
    subtitles_inclusion: FeatureInclusion
    lower_thirds_inclusion: FeatureInclusion
    music_inclusion: FeatureInclusion
    is_active: bool
    created_date_time: datetime
    modified_date_time: datetime

class VideoStream(BaseModel):
    src: str
    type: str
    video_format: VideoFormat

class BaseVideoContainer(BaseModel):
    id: str
    template: str
    hotlinking_protection_enabled: bool
    allowed_origins: List[str]
    video_stream: Optional[VideoStream]
    created_date_time: datetime
    modified_date_time: datetime

class VideoContainer(BaseVideoContainer):
    name: str
    description: Optional[str]

class Project(TakeOneProjectLite):
    video_container: str
    user: str
    state: str
    publishing_status: str

class CreateUserRequest(BaseModel):
    external_id: Optional[str]
    display_name: Optional[str]
    email_address: Optional[str]

class CreateVideoContainerRequest(BaseModel):
    template: str
    name: str
    description: Optional[str]
    hotlinking_protection_enabled: bool = False
    allowed_origins: List[str] = []

class CreateProjectRequest(BaseModel):
    user: str
    video_container: str
    organization_display_name: Optional[str]

class WebhookVideoContainer(BaseVideoContainer):
    pass

class WebhookProject(BaseModel):

    id: str
    video_container: str
    user: str
    state: str
    created_date_time: datetime
    modified_date_time: datetime

class WebhookType(str, Enum):
    PROJECT_STATUS_CHANGE = 'project_status_change'
    PROJECT_PUBLISHED = 'project_published'
    PROJECT_UNPUBLISHED = 'project_unpublished'
    PROJECT_PUBLISHING_ERROR = 'project_publishing_error'

class TakeOneWebhookRequest(BaseModel):
    type: WebhookType
    timestamp: int
    project: WebhookProject
    video_container: WebhookVideoContainer

class TakeOneClient:

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

        url = f'{self.base_url}/api/v1/app_users'
        r = httpx.post(
            url, 
            json=request.dict(exclude_none=True),
            auth=self.auth, 
            timeout=30
        )

        if r.status_code >= 400:
            response_body = r.json()
            print(response_body)

        r.raise_for_status()
        response_body = r.json()
        return User(**response_body)

    def create_video_container(
        self,
        request: CreateVideoContainerRequest
    ) -> VideoContainer:
        
        url = f'{self.base_url}/api/v1/video_containers'
        r = httpx.post(
            url, 
            json=request.dict(exclude_none=True),
            auth=self.auth, 
            timeout=30
        )

        if r.status_code == 400:
            response_body = r.json()
            print(response_body)

        r.raise_for_status()
        response_body = r.json()
        return VideoContainer(**response_body)
    
    def fetch_video_container(
        self,
        video_container_id: UUID
    ) -> VideoContainer:
        
        url = f'{self.base_url}/api/v1/video_containers/{video_container_id}'
        r = httpx.get(
            url, 
            auth=self.auth, 
            timeout=30
        )

        if r.status_code == 400:
            response_body = r.json()
            print(response_body)

        r.raise_for_status()
        response_body = r.json()
        return VideoContainer(**response_body)

    def create_project(
        self,
        request: CreateProjectRequest
    ) -> Project:

        url = f'{self.base_url}/api/v1/projects'
        r = httpx.post(
            url, 
            json=request.dict(exclude_none=True),
            auth=self.auth, 
            timeout=30
        )

        if r.status_code == 400:
            response_body = r.json()
            print(response_body)

        r.raise_for_status()
        response_body = r.json()
        return Project(**response_body)

    def authorize(
        self,
        user_id: str
    ) -> str:

        request = self.AuthorizationCodeRequest(
            user=user_id
        )

        url = f'{self.base_url}/api/v1/app_users/authorize'
        r = httpx.post(
            url, 
            json=request.dict(exclude_none=True),
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

