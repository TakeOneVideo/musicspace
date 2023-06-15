from typing import Any
import httpx
from models import *
import ffmpeg
import hashlib
import base64
import decimal
import json
import os

class AppUserTokenAuth(httpx.Auth):
    def __init__(self, access_token, refresh_token, base_url):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.base_url = base_url

    def build_refresh_request(self):
        url = f'{self.base_url}/sdkapi/v1/token'
        body = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        return httpx.post(url, json=body, timeout=None)

    def update_tokens(
        self,
        refresh_response
    ):
        token_response = TokenResponse(**refresh_response.json())
        self.access_token = token_response.access_token
        self.refresh_token = token_response.refresh_token

    def auth_flow(self, request):
        request.headers['Authorization'] = f'Bearer {self.access_token}'
        response = yield request

        if response.status_code == 401:
            # If the server issues a 401 response, then issue a request to
            # refresh tokens, and resend the request.
            refresh_response = yield self.build_refresh_request()
            self.update_tokens(refresh_response)

            request.headers['Authorization'] = f'Bearer {self.access_token}'
            yield request

def get_video_stats(video_filename: str) -> FFMPEGVideoStats:
    ## get probe result
    probe_result = ffmpeg.probe(video_filename)

    ## get first video stream
    streams = probe_result['streams']
    video_stream = None
    for stream in streams:
        if stream['codec_type'] == 'video':
            video_stream = stream
            break

    return FFMPEGVideoStats(**video_stream)

def _get_file_size(filename) -> int:
    return os.path.getsize(filename)

def _compute_md5(filename) -> str:
    with open(filename, 'rb') as file:
        m = hashlib.md5()
        b = file.read(4096)
        while len(b) > 0:
            m.update(b)
            b = file.read(4096)
        md5_data = m.digest()
    return base64.b64encode(md5_data).decode('utf-8')

# def create_app_user(
#     base_url: str,
#     credentials: ConfidentialClientCredentials,
#     user_info: AppUserConfig
# ) -> AppUserResponse:

#     url = f'{base_url}/api/v1/app_users'

#     r = httpx.post(url, json=user_info.dict(), auth=credentials.to_auth(), timeout=None)
#     if r.status_code >= 400:
#         print(f'An error occurred: {r.text}')
#     r.raise_for_status()

#     return AppUserResponse(**r.json())

# def create_video_container(
#     base_url: str,
#     credentials: ConfidentialClientCredentials,
#     video_container_config: VideoContainerConfig
# ) -> VideoContainerResponse:

#     url = f'{base_url}/api/v1/video_containers'

#     r = httpx.post(url, json=video_container_config.dict(exclude_none=True), auth=credentials.to_auth(), timeout=None)
#     if r.status_code >= 400:
#         print(f'An error occurred: {r.text}')
#     r.raise_for_status()

#     return VideoContainerResponse(**r.json())

# def create_project(
#     base_url: str,
#     credentials: ConfidentialClientCredentials,
#     user_id: str,
#     video_container_id: str,
#     organization_display_name: Optional[str]
# ) -> ProjectResponse:

#     url = f'{base_url}/api/v1/projects'

#     body = {
#         'user': user_id,
#         'video_container': video_container_id
#     }

#     if organization_display_name:
#         body['organization_display_name'] = organization_display_name

#     r = httpx.post(url, json=body, auth=credentials.to_auth(), timeout=None)
#     if r.status_code >= 400:
#         print(f'An error occurred: {r.text}')
#     r.raise_for_status()

#     return ProjectResponse(**r.json())

# def begin_app_user_authorization(
#     base_url: str,
#     credentials: ConfidentialClientCredentials,
#     user_id: str,
# ) -> AuthResponse:
    
#     url = f'{base_url}/api/v1/app_users/authorize'

#     body = {
#         'user': user_id
#     }

#     r = httpx.post(url, json=body, auth=credentials.to_auth(), timeout=None)
#     if r.status_code >= 400:
#         print(f'An error occurred: {r.text}')
#     r.raise_for_status()

#     return AuthResponse(**r.json())


# ## BEGIN APP USER
def complete_customer_api_user_authorization(
    base_url: str,
    code: str
) -> TokenResponse:
    url = f'{base_url}/sdkapi/v1/token'

    body = {
        'grant_type': 'authorization_code',
        'code': code
    }

    r = httpx.post(url, json=body, timeout=None)
    if r.status_code >= 400:
        print(f'An error occurred: {r.text}')
    r.raise_for_status()

    return TokenResponse(**r.json())

def create_video_segment(
    base_url: str,
    project_id: str,
    script: Optional[str], 
    auth: httpx.Auth
) -> VideoSegmentResponse:
    url = f'{base_url}/sdkapi/v1/projects/{project_id}/segments'

    body = {}
    if script:
        body['script'] = script

    r = httpx.post(url, auth=auth, json=body, timeout=None)
    if r.status_code >= 400:
        print(f'An error occurred: {r.text}')
    r.raise_for_status()

    return VideoSegmentResponse(**r.json())

def create_video_file_item_props(
    video_filename: str
) -> TakeVideoFileItemProps:
    
    ffmpeg_stats = get_video_stats(video_filename)
    content_length = _get_file_size(video_filename)
    content_md5 = _compute_md5(video_filename)

    quantized_video_length = decimal.Decimal(ffmpeg_stats.duration_in_seconds).quantize(decimal.Decimal('.1'), rounding=decimal.ROUND_UP)

    return TakeVideoFileItemProps(
        video_format=ffmpeg_stats.video_orientation,
        video_length=float(quantized_video_length),
        video_width=ffmpeg_stats.size.width,
        video_height=ffmpeg_stats.size.height,
        video_crf=0,
        video_frame_count=ffmpeg_stats.frame_count,
        video_frame_rate=ffmpeg_stats.frame_rate,
        file_format=FileFormat.MOV,
        file_object_content_length=content_length,
        file_object_content_md5=content_md5
    )

def create_take(
    base_url: str,
    project_id: str,
    video_segment_id: str,
    request: CreateTakeRequest,
    auth: httpx.Auth
) -> TakeResponse:
    url = f'{base_url}/sdkapi/v1/projects/{project_id}/segments/{video_segment_id}/takes'

    request_dict = request.dict(exclude_none=True)

    r = httpx.post(url, auth=auth, json=request_dict, timeout=None)
    if r.status_code >= 400:
        print(f'An error occurred: {r.text}')
    r.raise_for_status()

    return TakeResponse(**r.json())

def _get_tmp_filename(part_id):
    filename = f'./data/tmp/{part_id}'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return filename

def write_temp_file(
    input_file: str, 
    output_file: str, 
    offset: int, 
    length: int
):
    remaining_bytes = length
    with open(input_file, 'rb') as infile:
        infile.seek(offset)
        with open(output_file, 'wb') as outfile:
            b = infile.read(4096)
            while remaining_bytes > 0 and len(b) > 0:
                number_of_bytes_to_write = min(remaining_bytes, 4096)
                bytes_to_write = b[0:number_of_bytes_to_write]
                assert(len(bytes_to_write) == number_of_bytes_to_write)
                bytes_written = outfile.write(bytes_to_write)
                assert(len(bytes_to_write) == bytes_written)
                remaining_bytes = remaining_bytes - bytes_written
                b = infile.read(4096)

    assert(_get_file_size(output_file) == length)

def _upload_file(
    filename: str,
    presigned_post_request: PresignedPostRequest
) -> Any:

    with open(filename, 'rb') as file:
        files = {'file': file}

        r = httpx.post(
            presigned_post_request.url, 
            data=presigned_post_request.fields, 
            files=files
        )

        r.raise_for_status()
        response_text = r.text

        return response_text
    
def handle_video_segment(
    base_url: str,
    project_id: str,
    video_segment_config: VideoSegmentConfig, 
    auth: httpx.Auth
) -> VideoSegmentResponse:
    ## create video segment
    video_segment_response = create_video_segment(
        base_url=base_url,
        project_id=project_id,
        script=video_segment_config.script,
        auth=auth
    )

    ## add take to video segment
    video_file_item_props = create_video_file_item_props(
        video_filename=video_segment_config.take.video_filename
    )

    create_take_request = CreateTakeRequest(
        metadata=video_segment_config.take.metadata,
        video_file_item=video_file_item_props
    )

    take_response = create_take(
        base_url=base_url,
        project_id=project_id,
        video_segment_id=video_segment_response.id,
        request=create_take_request,
        auth=auth
    )

    video_upload_request = take_response.video_upload_request
    parts = video_upload_request.parts

    total_length = 0
    tmp_files = []
    for part in sorted(parts, key=lambda x: x.part_offset):

        if part.presigned_post_request is None:
            continue

        part_id = f'{take_response.id}-{part.part_offset}'
        tmp_file = _get_tmp_filename(part_id)
        tmp_files.append(tmp_file)

        write_temp_file(
            input_file=video_segment_config.take.video_filename, 
            output_file=tmp_file,
            offset=part.content_offset,
            length=part.content_length
        )

        part_content_length = _get_file_size(tmp_file)
        total_length = total_length + part_content_length

        _upload_file(
            filename=tmp_file,
            presigned_post_request=part.presigned_post_request
        )

    assert(total_length == video_file_item_props.file_object_content_length)
    return video_segment_response

def fetch_projects(
    base_url: str,
    auth: httpx.Auth
) -> ProjectsResponse:
    url = f'{base_url}/sdkapi/v1/projects'

    r = httpx.get(url, auth=auth, timeout=None)
    if r.status_code >= 400:
        print(f'An error occurred: {r.text}')
    r.raise_for_status()

    return ProjectsResponse(**r.json())

def create_production_request(
    base_url: str,
    project_id: str,
    request: CreateProductionRequestRequest,
    auth: httpx.Auth
) -> ProductionRequest:

    url = f'{base_url}/sdkapi/v1/projects/{project_id}/productionrequests'

    r = httpx.post(url, auth=auth, json=request.dict(exclude_none=True), timeout=None)
    if r.status_code >= 400:
        print(f'An error occurred: {r.text}')
    r.raise_for_status()

    response_json = r.json()

    return ProductionRequest(**response_json)

def fetch_production_request(
    base_url: str,
    project_id: str,
    production_request_id: str,
    auth: httpx.Auth
) -> ProductionRequest:

    url = f'{base_url}/sdkapi/v1/projects/{project_id}/productionrequests/{production_request_id}'

    r = httpx.get(url, auth=auth, timeout=None)
    if r.status_code >= 400:
        print(f'An error occurred: {r.text}')
    r.raise_for_status()

    response_json = r.json()

    return ProductionRequest(**response_json)

def submit_review(
    base_url: str,
    project_id: str,
    production_request_id: str,
    result: str,
    auth: httpx.Auth
) -> AppUserReview:
    url = f'{base_url}/sdkapi/v1/projects/{project_id}/user_reviews'

    body = {
        'result': result,
        'production_request': production_request_id
    }

    r = httpx.post(url, auth=auth, json=body, timeout=None)
    if r.status_code >= 400:
        print(f'An error occurred: {r.text}')
    r.raise_for_status()

    response_json = r.json()

    return AppUserReview(**response_json)