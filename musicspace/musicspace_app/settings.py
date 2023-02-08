from django.conf import settings

TAKEONE_BASE_URL = getattr(settings, 'TAKEONE_BASE_URL')
TAKEONE_CLIENT_ID = getattr(settings, 'TAKEONE_CLIENT_SECRET')
TAKEONE_CLIENT_SECRET = getattr(settings, 'TAKEONE_BASE_URL')

TAKEONE_PUBLIC_BASE_URL = getattr(settings, 'TAKEONE_PUBLIC_BASE_URL')
TAKEONE_PUBLIC_CLIENT_ID = getattr(settings, 'TAKEONE_PUBLIC_CLIENT_ID')