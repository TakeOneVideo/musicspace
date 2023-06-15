from typing import Any, Dict, List, Optional
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, HttpResponseBadRequest
from musicspace_app.models import Provider, Genre, Instrument, TakeOneProfileVideoContainer
from django.core.paginator import Paginator 
from dataclasses import dataclass, asdict, field
import urllib.parse
from enum import Enum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView, FormView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from musicspace_app.forms import AddressForm, ProviderForm, MusicspaceUserForm, EmptyForm
from django.db import transaction
from musicspace_app.domain import use_case_factory
import json
from django.core.exceptions import ObjectDoesNotExist
import musicspace_app.errors as app_errors

class ProviderPortalAuthMixin(UserPassesTestMixin, LoginRequiredMixin):
    login_url = 'musicspace:provider-login'
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.provider != None

    def handle_no_permission(self) -> HttpResponseRedirect:
        ## add a message
        messages.error(self.request, 'You must be a teacher to access this page')
        ## log the user out and let them try again
        logout(self.request)
        return super().handle_no_permission()

class ProviderPortalComponentAuthMixin(UserPassesTestMixin, LoginRequiredMixin):
    raise_exception = True
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.provider != None

class ProviderLoginView(LoginView):
    template_name = 'musicspace_app/login.html'
    next_page = 'musicspace:provider-profile'

    def get(self, request, *args, **kwargs):
        redirect_url = self.request.GET.get(self.redirect_field_name, '')
        if redirect_url:
            return super().get(request, *args, **kwargs)
        else:
            current_page = reverse('musicspace:provider-login')
            next_page = reverse(self.next_page)
            return redirect(f'{current_page}?{self.redirect_field_name}={next_page}')

class ProviderLogoutView(LogoutView):
    next_page ='musicspace:index'

class Modality(str, Enum):
    IN_PERSON_ONLY = 'in_person_only'
    ONLINE_ONLY = 'online_only'
    EITHER = 'either'

@dataclass
class QueryParameters:
    modality: Modality = Modality.EITHER
    genre: List[str] = field(default_factory=list)
    instrument: List[str] = field(default_factory=list)

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
        d: QueryDict
    ) -> QueryParameters:
        return QueryParameters(
            modality=d.get('modality'),
            genre=d.getlist('genre'),
            instrument=d.getlist('instrument')
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
        query_string = urllib.parse.urlencode(query_dict, doseq=True)
        return "%s?%s" % (base_url, query_string)

    def get_queryset(
        self,
        query_params: QueryParameters
    ):
        providers_queryset = Provider.objects.all()

        if query_params.modality == Modality.IN_PERSON_ONLY:
            providers_queryset = providers_queryset.exclude(
                in_person=False
            )

        elif query_params.modality == Modality.ONLINE_ONLY:
            providers_queryset = providers_queryset.exclude(
                online=False
            )

        ## if genres are selected, we want to include teachers that match ANY of the genres
        if query_params.genre:
            providers_queryset = providers_queryset.filter(
                genres__in=query_params.genre
            ).distinct()

        if query_params.instrument:
            providers_queryset = providers_queryset.filter(
                instruments__in=query_params.instrument
            ).distinct()
                

        providers_queryset = providers_queryset.select_related('user', 'location')\
            .order_by('user__date_joined')

        return providers_queryset
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # print(self.request.GET)
        if not self.request.GET:
            query_params = QueryParameters()
        else:
            query_params = self._generate_query_params_from_input(
                d=self.request.GET
            )

        # print(query_params)
        # print(type(query_params.genre))
        # print(query_params.genre)

        context['query_params'] = query_params
        context['genres'] = Genre.objects.all()
        context['instruments'] = Instrument.objects.all()

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

        # print(self.request.POST)
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

    def get_takeone_profile_video_container(
        self, 
        provider: Provider
    ) -> Optional[TakeOneProfileVideoContainer]:
        try:
            takeone_user = provider.takeone_user
            if takeone_user:
                return takeone_user.profile_video_container
            else:
                return None
        except ObjectDoesNotExist:
            return None

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        provider = self.get_provider()
        context['provider'] = provider
        context['takeone_profile_video_container'] = self.get_takeone_profile_video_container(provider)

        return context

class ForProvidersView(TemplateView):
    template_name = 'musicspace_app/for_providers.html'

class ProviderProfileView(ProviderPortalAuthMixin, TemplateView):

    template_name = 'musicspace_app/provider_profile.html'

    def get_provider(self) -> Provider:
        return self.request.user.provider

    def get_takeone_profile_video_container(
        self, 
        provider: Provider
    ) -> Optional[TakeOneProfileVideoContainer]:
        try:
            takeone_user = provider.takeone_user
            if takeone_user:
                return takeone_user.profile_video_container
            else:
                return None
        except ObjectDoesNotExist:
            return None

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        provider = self.get_provider()
        context['address_form'] = AddressForm(instance=provider.location)
        context['provider_form'] = ProviderForm(instance=provider)
        context['user_form'] = MusicspaceUserForm(instance=provider.user)
        
        takeone_profile_video_container = self.get_takeone_profile_video_container(provider=provider)

        if takeone_profile_video_container:

            ## NOTE - if webhooks are used, this refreshing from the server would be unnecessary
            takeone_project_use_case = use_case_factory.takeone_project_use_case()
            takeone_profile_video_container = takeone_project_use_case.update_video_container_from_server(
                video_container=takeone_profile_video_container
            )

            context['takeone_profile_video_container'] = takeone_profile_video_container
            
        return context

    def post(self, request, *args, **kwargs):
        provider = self.get_provider()
        address_form = AddressForm(self.request.POST, instance=provider.location)
        provider_form = ProviderForm(self.request.POST, instance=provider)
        user_form = MusicspaceUserForm(self.request.POST, instance=provider.user)

        if address_form.is_valid() and provider_form.is_valid() and user_form.is_valid():
            with transaction.atomic():
                address_form.save()
                provider_form.save()
                user_form.save()
                return HttpResponseRedirect(self.request.path)
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

class AddVideoView(ProviderPortalComponentAuthMixin, FormView):
    template_name = None
    form_class = EmptyForm

    def get_provider(self) -> Provider:
        return self.request.user.provider

    def form_valid(self, form):

        provider = self.get_provider()
        ## this needs to create a user and a project
        takeone_user_use_case = use_case_factory.takeone_user_use_case()
        takeone_user = provider.takeone_user
        if not takeone_user:
            takeone_user = takeone_user_use_case.create_user(
                provider=provider
            )

        takeone_project_use_case = use_case_factory.takeone_project_use_case()
        ## create video container
        profile_video_container = takeone_project_use_case.create_profile_video_container(
            takeone_user=takeone_user
        )

        ## create the project
        takeone_project = takeone_project_use_case.create_project(
            takeone_user=takeone_user,
            video_container=profile_video_container
        )

        ## send email to user
        takeone_user_use_case.send_invitation_email(
            takeone_user=takeone_user
        )

        response = HttpResponse()
        response["HX-Refresh"] = "true"

        return response

    def form_invalid(self, form) -> HttpResponse:
        return HttpResponseBadRequest()

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return self.http_method_not_allowed(request, *args, **kwargs)
    
class ResendInvitationView(ProviderPortalComponentAuthMixin, FormView):
    template_name = None
    form_class = EmptyForm

    def get_provider(self) -> Provider:
        return self.request.user.provider

    def form_valid(self, form):

        provider = self.get_provider()
        takeone_user = provider.takeone_user
        if not takeone_user:
            raise app_errors.BadRequestError()

        ## send email to user
        takeone_user_use_case = use_case_factory.takeone_user_use_case()
        takeone_user_use_case.send_invitation_email(
            takeone_user=takeone_user
        )

        response = HttpResponse()
        response["HX-Refresh"] = "true"

        return response

    def form_invalid(self, form) -> HttpResponse:
        return HttpResponseBadRequest()

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return self.http_method_not_allowed(request, *args, **kwargs)

class AboutUsView(TemplateView):
    template_name = 'musicspace_app/about_us.html'

# class IndexView(TemplateView):
#     template_name = 'musicspace_app/index.html'

class IndexView(ProviderListView):
    pass

class TakeOneWebhookView(APIView):

    def post(self, request, *args,  **kwargs):

        print(json.dumps(request.data, indent=4))
        takeone_project_use_case = use_case_factory.takeone_project_use_case()
        try:
            webhook_request = takeone_project_use_case.decode_webhook_request(
                webhook_request_dict=request.data
            )
        except BaseException as e:
            print('got exception')
            print(e)
            return Response({}, status=status.HTTP_200_OK)

        try:
            takeone_project_use_case.handle_webhook(
                webhook_request=webhook_request
            )
        except BaseException as e:
            print('got exception')
            print(e)

        return Response({}, status=status.HTTP_200_OK)