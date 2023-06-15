
from typing import Optional, List, Tuple
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

# class ConfidentialClientCredentials(BaseModel):
#     client_id: str
#     client_secret: str

#     def to_auth(self) -> Tuple[str, str]:
#         return (self.client_id, self.client_secret)

class VideoFormat(str, Enum):
    LANDSCAPE = 'landscape'
    PORTRAIT = 'portrait'
    SQUARE = 'square'

class FileFormat(str, Enum):
    MOV = 'mov'
    PNG = 'png'
    JPEG = 'jpg'
    TIFF = 'tiff'
    WAV = 'wav'
    MP3 = 'mp3'
    ZIP = 'zip'

    @property
    def content_type(self):
        if self == self.JPEG:
            return f'image/jpeg'
        elif self == self.MOV:
            return f'video/quicktime'
        elif self == self.WAV:
            return 'audio/wave'
        elif self == self.MP3:
            return 'audio/mpeg'
        elif self == self.ZIP:
            return 'application/zip'
        else:
            return f'image/{self.value}'

    @property
    def file_extension(self) -> str:
        return self.value


class Size(BaseModel):
    width: int
    height: int

# class AppUserConfig(BaseModel):
#     external_id: Optional[str]
#     display_name: Optional[str]
#     email_address: Optional[str]

# class VideoContainerConfig(BaseModel):
#     template: str
#     name: str
#     description: Optional[str]

class TakeConfig(BaseModel):
    metadata: Optional[dict]
    video_filename: str

class VideoSegmentConfig(BaseModel):
    script: Optional[str]
    take: TakeConfig
    
# class APIClientProjectConfig(BaseModel):
#     organization_display_name: Optional[str]

class AppUserProjectConfig(BaseModel):
    user_provided_title: Optional[str]
    script: Optional[str]
    video_segments: List[VideoSegmentConfig]

class ProductionRequestParams(BaseModel):
    music: Optional[str]
    add_subtitles: bool
    name: Optional[str]
    title: Optional[str]

# class APIClientWorkflowConfig(BaseModel):
#     base_url: str
#     credentials: ConfidentialClientCredentials
#     user: AppUserConfig
#     video_container: VideoContainerConfig
#     project: APIClientProjectConfig

class AppUserWorkflowConfig(BaseModel):
    base_url: str
    project: AppUserProjectConfig
    production_request: ProductionRequestParams

# class AppUserResponse(BaseModel):
#     id: str

# class VideoContainerResponse(BaseModel):
#     id: str

class ProjectResponse(BaseModel):
    id: str
    script: Optional[str]

class ProjectsResponse(BaseModel):
    results: List[ProjectResponse]

# class AuthResponse(BaseModel):
#     code: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class VideoSegmentResponse(BaseModel):
    id: str
    script: Optional[str]

class FFMPEGVideoStats(BaseModel):
    width: int
    height: int
    frame_rate: str
    avg_frame_rate: str
    nb_frames: str
    duration: str

    @property
    def frames_per_second(self) -> float:
        frame_rate_split = self.frame_rate.split('/')
        return float(frame_rate_split[0]) / float(frame_rate_split[1])

    @property
    def rounded_frames_per_second(self) -> int:
        return round(self.frames_per_second)

    @property
    def rounded_frame_rate(self) -> str:
        return f'{self.rounded_frames_per_second}/1'

    @property
    def frame_count(self):
        return int(self.nb_frames)

    @property
    def duration_in_seconds(self):
        return float(self.duration)
    
    class Config:
        fields = {
            'frame_rate': 'r_frame_rate'
        }

    @property
    def size(self) -> Size:
        return Size(
            width=self.width,
            height=self.height
        )

    @property
    def video_orientation(self) -> VideoFormat:
        size = self.size
        if size.width > size.height:
            return VideoFormat.LANDSCAPE
        elif size.width < size.height:
            return VideoFormat.PORTRAIT
        else:
            return VideoFormat.SQUARE
        
class TakeVideoFileItemProps(BaseModel):
    video_format: VideoFormat
    video_length: float
    video_width: int
    video_height: int
    video_crf: int
    video_frame_count: int
    video_frame_rate: str
    file_format: FileFormat
    file_object_content_length: int
    file_object_content_md5: str

class CreateTakeRequest(BaseModel):
    metadata: Optional[dict] = None
    video_file_item: TakeVideoFileItemProps


class PresignedPostRequest(BaseModel):
    url: str
    fields: dict

class VideoUploadRequestPart(BaseModel):
    state: str
    part_offset: int
    content_offset: int
    content_length: int
    presigned_post_request: Optional[PresignedPostRequest]

class VideoUploadRequest(BaseModel):
    state: str
    parts: List[VideoUploadRequestPart]

class TakeResponse(BaseModel):
    id: str
    video_upload_request: VideoUploadRequest
    metadata: Optional[dict]

class CreateProductionRequestRequest(BaseModel):
    video_segments: List[str]
    music: Optional[str]
    add_subtitles: bool
    name: Optional[str]
    title: Optional[str]

class ProductionRequestVideoRun(BaseModel):
    state: str
    output_video_format: VideoFormat
    editing_progress: float
    post_processing_progress: float
    streaming_url: Optional[str]

class ProductionRequest(BaseModel):
    id: str
    state: str
    coloring_progress: float
    editing_progress: float
    post_processing_progress: float
    project: str
    video_runs: List[ProductionRequestVideoRun]

class AppUserReview(BaseModel):
    id: str
    result: str
    project: str
    production_request: str
    reviewer: str

