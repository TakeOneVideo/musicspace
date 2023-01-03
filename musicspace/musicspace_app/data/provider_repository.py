from musicspace_app.models import ProviderFile, Provider
from typing import List, Optional
from uuid import UUID

class ProviderRepository:

    def __init__(
        self,
        providers_fixture_filename: str
    ):
        providers_fixture_file = ProviderFile.parse_file(providers_fixture_filename)

        self.provider_map = { provider.id: provider for provider in providers_fixture_file.providers }

        print(self.provider_map)

    def get_providers(self) -> List[Provider]:
        return sorted(self.provider_map.values(), key=lambda provider: provider.created_date_time)

    def get_provider(self, provider_id: UUID) -> Optional[Provider]:
        return self.provider_map.get(provider_id)