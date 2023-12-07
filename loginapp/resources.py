from import_export import resources
from .models import Student, Classroom, Teacher, Course, Course_Selection


class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('className', 'studID', 'name', 'email')

class ClassroomResource(resources.ModelResource):
    class Meta:
        model = Classroom


class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher


class CourseResource(resources.ModelResource):
    class Meta:
        model = Course


class Course_SelectionResource(resources.ModelResource):
    class Meta:
        model = Course_Selection
