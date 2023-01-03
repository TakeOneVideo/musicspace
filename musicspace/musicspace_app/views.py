from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import Http404
from django.shortcuts import get_object_or_404
from musicspace_app.models import Provider
# Create your views here.
class ProviderListView(TemplateView):
    template_name = 'musicspace_app/provider_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['providers'] = Provider.objects.all()\
            .select_related('user', 'location')
        return context

class ProviderDetailView(TemplateView):
    template_name = 'musicspace_app/provider_detail.html'

    def get_provider(self) -> Provider:
        return get_object_or_404(Provider.objects.select_related('user', 'location'), id=self.kwargs['provider_id'])

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['provider'] = self.get_provider()
        return context

class ForProvidersView(TemplateView):
    template_name = 'musicspace_app/for_providers.html'

class AboutUsView(TemplateView):
    template_name = 'musicspace_app/about_us.html'

class IndexView(ProviderListView):
    pass