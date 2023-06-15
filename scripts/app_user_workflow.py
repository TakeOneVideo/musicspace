import argparse
import json
from time import sleep
import common
import logging
import models
from typing import List
logger = logging.getLogger()
logger.setLevel('DEBUG')

def main():

    parser = argparse.ArgumentParser(description='Full workflow')
    parser.add_argument('config_file', help='Config file')
    parser.add_argument('code', help='App User Auth Code')

    args = parser.parse_args()
    config: models.AppUserWorkflowConfig = models.AppUserWorkflowConfig.parse_file(args.config_file)

    ## complete auth
    print(f'Completing app user auth process')
    token_response = common.complete_customer_api_user_authorization(
        base_url=config.base_url,
        code=args.code
    )
    print(f'App user auth process completed')

    ## create httpx token auth object
    auth = common.AppUserTokenAuth(
        access_token=token_response.access_token,
        refresh_token=token_response.refresh_token,
        base_url=config.base_url
    )

    ## fetch user projects 
    ## results are reverse chron order
    projects_response = common.fetch_projects(
        base_url=config.base_url,
        auth=auth
    )

    ## get latest project
    project = projects_response.results[0]

    ## handle video segments
    video_segments: List[str] = []
    for video_segment_config in config.project.video_segments:
        video_segment = common.handle_video_segment(
            base_url=config.base_url,
            project_id=project.id,
            video_segment_config=video_segment_config,
            auth=auth
        )

        video_segments.append(str(video_segment.id))

    ## Create production request
    request = models.CreateProductionRequestRequest(
        video_segments=video_segments,
        music=config.production_request.music,
        add_subtitles=config.production_request.add_subtitles,
        name=config.production_request.name,
        title=config.production_request.title
    )

    production_request = common.create_production_request(
        base_url=config.base_url,
        project_id=project.id,
        request=request,
        auth=auth
    )

    while production_request.state != 'completed' and production_request.state != 'error':
        sleep(30)
        production_request = common.fetch_production_request(
            base_url=config.base_url,
            project_id=project.id,
            production_request_id=production_request.id,
            auth=auth
        )

        print(f'Production request is in the {production_request.state} state.')
        print(f'Coloring progress is {production_request.coloring_progress}')
        print(f'Editing progress is {production_request.editing_progress}')
        print(f'Post processing progress is {production_request.post_processing_progress}')

    ## once completed, submit review
    user_review = common.submit_review(
        base_url=config.base_url,
        project_id=project.id,
        production_request_id=production_request.id,
        result='accepted',
        auth=auth
    )



if __name__ == "__main__":
    main()
