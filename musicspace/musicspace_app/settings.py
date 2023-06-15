from django.conf import settings

TAKEONE_BASE_URL = getattr(settings, 'TAKEONE_BASE_URL')
TAKEONE_CLIENT_ID = getattr(settings, 'TAKEONE_CLIENT_ID')
TAKEONE_CLIENT_SECRET = getattr(settings, 'TAKEONE_CLIENT_SECRET')
TAKEONE_VIDEO_CONTAINER_TEMPLATE_ID = getattr(settings, 'TAKEONE_VIDEO_CONTAINER_TEMPLATE_ID')

FROM_EMAIL = getattr(settings, 'FROM_EMAIL')