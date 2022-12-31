from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.base import TemplateView
from musicspace_app.data.provider_repository import ProviderRepository

# Create your views here.
class ProviderListView(TemplateView):
    template_name = 'musicspace_app/provider_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        provider_repository = ProviderRepository(providers_fixture_filename='/src/musicspace_app/fixtures/providers.json')
        print(provider_repository.providers)
        context['providers'] = provider_repository.providers
        return context

class ProviderDetailView(TemplateView):
    template_name = 'musicspace_app/provider_detail.html'

class ForProvidersView(TemplateView):
    template_name = 'musicspace_app/for_providers.html'

class AboutUsView(TemplateView):
    template_name = 'musicspace_app/about_us.html'

class IndexView(ProviderListView):
    pass