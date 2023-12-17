from import_export import resources, fields
from .models import Student, Classroom, Teacher, Course, Course_Selection
from django.contrib.auth.hashers import make_password
from import_export.widgets import ForeignKeyWidget
class StudentResource(resources.ModelResource):
    # password = fields.Field(column_name='password', attribute='password', widget=widgets.CharWidget())
    class Meta:
        model = Student
        fields = ('className', 'studentID', 'name','password', 'email', 'is_student', 'is_teacher')
        import_id_fields = ['studentID']
        export_order = ('className', 'studentID', 'name','password', 'email', 'is_student', 'is_teacher')
        import_order = ('className', 'studentID', 'name','password', 'email', 'is_student', 'is_teacher')

    def before_save_instance(self, instance, using_transactions, dry_run):
        # 檢查密碼是否已經被哈希化
        if not dry_run and 'password' in instance.changed_fields and not instance.password.startswith('bcrypt$'):
            # 如果密碼未被哈希化，使用 make_password 函數對其進行哈希化
            instance.password = make_password(instance.password)
        # 調用 super 方法，執行原始的保存邏輯
        super().before_save_instance(instance, using_transactions, dry_run)

class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher
        import_id_fields = ['teacher_key']


class CourseResource(resources.ModelResource):
    teacher_key = fields.Field(
        column_name='teacher_key',
        attribute='teacher_key',
        widget=ForeignKeyWidget(Teacher, 'teacher_key'))
    
    classroom = fields.Field(
        column_name='classroom',
        attribute='classroom',
        widget=ForeignKeyWidget(Classroom, 'classroom_key'))

    class Meta:
        model = Course
        fields = ('course_key', 'teacher_key', 'course_name', 'department', 'course_grade', 'course_className', 'classroom', 'seat', 'day_of_week', 'class_time')
        import_id_fields = ['course_key']
        export_order = fields  # 保持与 fields 一致
        export_encoding = 'utf-8-sig'  # 设置导出编码为 UTF-8

class Course_SelectionResource(resources.ModelResource):
    class Meta:
        model = Course_Selection
        import_id_fields = ['ID']

class ClassroomResource(resources.ModelResource):
    class Meta:
        model = Classroom
        import_id_fields = ['classroom_key']