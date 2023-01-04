from typing import Any, Dict, List, Optional
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from musicspace_app.models import Provider
from django.core.paginator import Paginator 
from dataclasses import dataclass, asdict
import urllib.parse
from enum import Enum


class Modality(str, Enum):
    IN_PERSON_ONLY = 'in_person_only'
    ONLINE_ONLY = 'online_only'
    EITHER = 'either'

@dataclass
class QueryParameters:
    modality: Modality = Modality.EITHER

DEFAULT_PAGE_SIZE = 10
class ProviderListView(TemplateView):

    ## this needs to differentiate between the initial load
    ## the filters being updated
    ## and another page being loaded
    def get_template_names(self) -> List[str]:
        if self.request.htmx:
            if self.request.htmx.trigger == 'provider-search-filter':
                return 'musicspace_app/components/provider_search_results.html'
            else:
                return 'musicspace_app/components/provider_list.html'
        else:
            return 'musicspace_app/provider_search.html'

    def _generate_query_params_from_input(
        self,
        d: Dict
    ) -> QueryParameters:
        print(d)
        return QueryParameters(
            modality=d.get('modality')
        )

    def _generate_url_from_query_params(
        self,
        query_params: QueryParameters,
        next_page_index: Optional[int] = None
    ) -> str:
        base_url = reverse('musicspace:provider-list')

        ## we should probably only include these if they are different than defaults
        query_dict = {key: value for (key, value) in asdict(query_params).items() if value is not None} 
        if next_page_index:
            query_dict['page'] = next_page_index
        query_string = urllib.parse.urlencode(query_dict)
        return "%s?%s" % (base_url, query_string)

    def get_queryset(
        self,
        query_params: QueryParameters
    ):
        providers_queryset = Provider.objects.all()

        print(query_params)

        if query_params.modality == Modality.IN_PERSON_ONLY:
            providers_queryset = providers_queryset.exclude(
                in_person=False
            )

        elif query_params.modality == Modality.ONLINE_ONLY:
            providers_queryset = providers_queryset.exclude(
                online=False
            )

        providers_queryset = providers_queryset.select_related('user', 'location')\
            .order_by('user__date_joined')

        return providers_queryset
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        print(self.request.GET)
        if not self.request.GET:
            query_params = QueryParameters()
        else:
            query_params = self._generate_query_params_from_input(
                d=self.request.GET
            )

        context['query_params'] = query_params

        providers_queryset = self.get_queryset(query_params=query_params)
        paginator = Paginator(providers_queryset, DEFAULT_PAGE_SIZE)

        page_number = int(self.request.GET.get('page', 1))
        context['page_of_providers'] = paginator.get_page(page_number)

        next_page_index = page_number + 1
        if next_page_index <= paginator.num_pages:
            
            context['next_page_url'] = self._generate_url_from_query_params(
                query_params=query_params,
                next_page_index=next_page_index
            )


        context['total_provider_count'] = paginator.count

        return context

    ## extract form params, compute url and redirect
    def post(self, request, *args, **kwargs):

        print(self.request.POST)
        query_params = self._generate_query_params_from_input(
            d=self.request.POST
        )

        url = self._generate_url_from_query_params(query_params)
        print(url)
        return HttpResponseRedirect(url)

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