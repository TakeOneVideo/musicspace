from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class InstructorListView(TemplateView):
    template_name = 'musicspace_app/instructor_list.html'

class InstructorDetailView(TemplateView):
    template_name = 'musicspace_app/instructor_detail.html'

class ForTeachersView(TemplateView):
    template_name = 'musicspace_app/for_teachers.html'

class AboutUsView(TemplateView):
    template_name = 'musicspace_app/about_us.html'

class IndexView(InstructorListView):
    pass