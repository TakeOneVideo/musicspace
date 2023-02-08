from musicspace_app import settings

def takeone_public_video_config_processor(request):
    return {
        'TAKEONE_PUBLIC_BASE_URL': settings.TAKEONE_PUBLIC_BASE_URL,
        'TAKEONE_PUBLIC_CLIENT_ID': settings.TAKEONE_PUBLIC_CLIENT_ID
    }