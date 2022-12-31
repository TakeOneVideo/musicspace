from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.base import TemplateView
from musicspace_app.data.teacher_repository import TeacherRepository

# Create your views here.
class InstructorListView(TemplateView):
    template_name = 'musicspace_app/instructor_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        teacher_repository = TeacherRepository(teachers_fixture_filename='/src/musicspace_app/fixtures/teachers.json')
        print(teacher_repository.teachers)

        return super().get_context_data(**kwargs)

class InstructorDetailView(TemplateView):
    template_name = 'musicspace_app/instructor_detail.html'

class ForTeachersView(TemplateView):
    template_name = 'musicspace_app/for_teachers.html'

class AboutUsView(TemplateView):
    template_name = 'musicspace_app/about_us.html'

class IndexView(InstructorListView):
    pass