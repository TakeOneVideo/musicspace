from django.conf import settings
from .data import TakeOneClient

takeone_client = TakeOneClient(
    base_url=settings.TAKEONE_BASE_URL,
    client_id=settings.TAKEONE_CLIENT_ID,
    client_secret=settings.TAKEONE_CLIENT_SECRET
)