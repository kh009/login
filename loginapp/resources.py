from import_export import resources, fields, widgets
from .models import Student, Classroom, Teacher, Course, Course_Selection
from django.contrib.auth.hashers import make_password
class StudentResource(resources.ModelResource):
    # password = fields.Field(column_name='password', attribute='password', widget=widgets.CharWidget())
    class Meta:
        model = Student
        fields = ('className', 'studentID', 'name','password', 'email', 'is_student', 'is_teacher')
        import_id_fields = ['studentID']
        export_order = ('className', 'studentID', 'name','password', 'email', 'is_student', 'is_teacher')
        import_order = ('className', 'studentID', 'name','password', 'email', 'is_student', 'is_teacher')

    def before_save_instance(self, instance, using_transactions, dry_run):
        # 检查密码是否已经被哈希化
        if not dry_run and 'password' in instance.changed_fields and not instance.password.startswith('bcrypt$'):
            # 如果密码未被哈希化，使用 make_password 函数对其进行哈希化
            instance.password = make_password(instance.password)
        # 调用 super 方法，执行原始的保存逻辑
        super().before_save_instance(instance, using_transactions, dry_run)



class ClassroomResource(resources.ModelResource):
    class Meta:
        model = Classroom


class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher


class CourseResource(resources.ModelResource):
    class Meta:
        model = Course
        import_id_fields = ['course_key']

class Course_SelectionResource(resources.ModelResource):
    class Meta:
        model = Course_Selection
        