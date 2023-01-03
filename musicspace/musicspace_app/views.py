from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import Http404
from musicspace_app.data.provider_repository import ProviderRepository

provider_repository = ProviderRepository(providers_fixture_filename='/src/musicspace_app/fixtures/providers.json')

# Create your views here.
class ProviderListView(TemplateView):
    template_name = 'musicspace_app/provider_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['providers'] = provider_repository.get_providers()
        return context

class ProviderDetailView(TemplateView):
    template_name = 'musicspace_app/provider_detail.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        provider_id = kwargs['provider_id']
        provider = provider_repository.get_provider(provider_id=provider_id)
        if not provider:
            return Http404()

        context['provider'] = provider
        return context

class ForProvidersView(TemplateView):
    template_name = 'musicspace_app/for_providers.html'

class AboutUsView(TemplateView):
    template_name = 'musicspace_app/about_us.html'

class IndexView(ProviderListView):
    pass