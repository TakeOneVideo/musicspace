from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import Http404
from django.shortcuts import get_object_or_404
from musicspace_app.models import Provider
from django.core.paginator import Paginator
# Create your views here.

DEFAULT_PAGE_SIZE = 10
class ProviderSearchView(TemplateView):
    template_name = 'musicspace_app/provider_search.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        providers = Provider.objects.all()\
            .select_related('user', 'location')\
            .order_by('user__date_joined')
        paginator = Paginator(providers, DEFAULT_PAGE_SIZE)

        page_number = int(self.request.GET.get('page', 1))
        context['page_of_providers'] = paginator.get_page(page_number)
        next_page_index = page_number + 1
        if next_page_index <= paginator.num_pages:
            context['next_page_index'] = next_page_index

        context['total_provider_count'] = paginator.count

        return context

class ProviderListComponentView(TemplateView):
    template_name = 'musicspace_app/components/provider_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        providers = Provider.objects.all()\
            .select_related('user', 'location')\
            .order_by('user__date_joined')
        paginator = Paginator(providers, DEFAULT_PAGE_SIZE)
        page_number = int(self.request.GET.get('page', 1))
        page_of_providers = paginator.get_page(page_number)
        context['page_of_providers'] = page_of_providers
        next_page_index = page_number + 1
        if next_page_index <= paginator.num_pages:
            context['next_page_index'] = next_page_index
        
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

class IndexView(ProviderSearchView):
    pass