from musicspace_app.models import ProviderFile, Provider

class ProviderRepository:

    def __init__(
        self,
        providers_fixture_filename: str
    ):
        providers_fixture_file = ProviderFile.parse_file(providers_fixture_filename)
        self.providers = providers_fixture_file.providers

        print(self.providers)