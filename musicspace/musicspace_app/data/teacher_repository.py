from musicspace_app.models import TeacherFile, Teacher

class TeacherRepository:

    def __init__(
        self,
        teachers_fixture_filename: str
    ):
        teachers_fixture_file = TeacherFile.parse_file(teachers_fixture_filename)
        self.teachers = teachers_fixture_file.teachers

        print(self.teachers)