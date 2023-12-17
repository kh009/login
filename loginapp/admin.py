from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import StudentResource,CourseResource,Course_SelectionResource,TeacherResource,ClassroomResource
# Register your models here.

admin.site.site_header = '點名系統管理後台'  # 設置標頭
admin.site.site_title = '點名系統管理後台'   # 設置標題
admin.site.index_title = '點名系統管理後台'

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('className', 'studentID', 'name', 'email')
    resource_class = StudentResource

@admin.register(Classroom)
class ClassroomAdmin(ImportExportModelAdmin):
    list_display = ('classroom_key', 'seat')
    resource_class = ClassroomResource

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    list_display = ('teacher_key', 'teacher_name', 'job_title',
                    'teacher_email', 'phone', 'seat')
    resource_class = TeacherResource

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    list_display = ('course_key', 'teacher_key', 'course_name',
                    'department', 'course_grade', 'course_className', 'classroom')
    resource_class = CourseResource


@admin.register(Course_Selection)
class Course_SelectionAdmin(ImportExportModelAdmin):
    list_display = ('course_key', 'studentID')
    resource_class = Course_SelectionResource

@admin.register(Course_seat)
class Course_seatAdmin(ImportExportModelAdmin):
    list_display = ('student', 'number','course','week_number')


