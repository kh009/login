from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password

# Create your models here.


class Student(models.Model):
    className = models.CharField(max_length=20, verbose_name='班級名稱')
    studentID = models.CharField(max_length=10, primary_key=True, verbose_name='學號')
    name = models.CharField(max_length=30, verbose_name='姓名')
    password = models.CharField(max_length=128, verbose_name='密碼')
    email = models.EmailField(max_length=254, verbose_name='email')
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # 在保存之前使用 make_password 将密码哈希化
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '學生'
        verbose_name_plural = '學生列表'


class Classroom(models.Model):
    classroom_key = models.CharField(max_length=20, primary_key=True, verbose_name='教室代碼')
    seat = models.IntegerField(default=0, verbose_name='座位')

    def __str__(self):
        return self.classroom_key

    class Meta:
        verbose_name = '教室'
        verbose_name_plural = '教室列表'


class Teacher(models.Model):
    teacher_key = models.CharField(max_length=20, primary_key=True, verbose_name='教師代碼')
    password = models.CharField(max_length=128, default="123", verbose_name='密碼')
    teacher_name = models.CharField(max_length=4, verbose_name='姓名')
    job_title = models.CharField(max_length=5, verbose_name='職稱')
    teacher_email = models.EmailField(default="12346", max_length=254, verbose_name='email')
    phone = models.CharField(max_length=20, verbose_name='電話')
    seat = models.CharField(max_length=20, verbose_name='研究室位置')
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # 在保存之前使用 make_password 将密码哈希化
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.teacher_name

    class Meta:
        verbose_name = '老師'
        verbose_name_plural = '老師列表'


class Course(models.Model):
    course_key = models.CharField(
        max_length=20, primary_key=True, default="", verbose_name="課程代碼")  # 課程代碼
    teacher_key = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, verbose_name="教師代碼")  # 教師代碼
    course_name = models.CharField(max_length=20, verbose_name="課程名稱")  # 課程名稱
    department = models.CharField(max_length=20, verbose_name="科系")  # 科系
    course_grade = models.CharField(max_length=20, verbose_name="年級")  # 年級
    course_className = models.CharField(max_length=20, verbose_name="班別")  # 班別
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, verbose_name="教室代碼")  # 教室代碼
    seat = models.IntegerField(default=0, verbose_name="座位")  # 座位
    DAY_CHOICES = [
        (1, '星期一'),
        (2, '星期二'),
        (3, '星期三'),
        (4, '星期四'),
        (5, '星期五'),
        (6, '星期六'),
        (7, '星期天'),
    ]
    day_of_week = models.IntegerField(choices=DAY_CHOICES, default=1)
    class_time = models.TimeField(null=True, blank=True)  # 上課時間，默认为null，可以为空

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = '課程'
        verbose_name_plural = '課程列表'


class Course_seat(models.Model):
    WEEK_CHOICES = [(i, f'{i}周') for i in range(1, 19)]  # 生成1到18周的选择项
    id = models.AutoField(primary_key=True, verbose_name='ID')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='學生')
    number = models.IntegerField(default=0, null=True, verbose_name='座位號')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='課程')
    is_absent = models.BooleanField(default=False, verbose_name='是否缺席')
    selection_time = models.DateTimeField(null=True, verbose_name='選課時間')
    week_number = models.IntegerField(choices=WEEK_CHOICES, default=1, verbose_name='周數')
    # 添加第一周的起始时间，这里假设第一周开始于2023年1月1日

    FIRST_WEEK_START_TIME = datetime(2023, 1, 1)

    def get_week_start_time(self):
        # 计算第一周的起始时间
        first_week_start_time = self.FIRST_WEEK_START_TIME

        # 计算当前周的起始时间
        current_week_start_time = first_week_start_time + \
            timedelta(weeks=self.week_number - 1)

        return current_week_start_time

    def __str__(self):
        return self.student.name

    class Meta:
        verbose_name = '選課座位'
        verbose_name_plural = '選課座位列表'


class Course_Selection(models.Model):
    course_key = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='課程代碼')
    studentID = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name='學生')

    class Meta:
        unique_together = ['course_key', 'studentID']
        verbose_name = '課程選課'
        verbose_name_plural = '課程選課列表'
