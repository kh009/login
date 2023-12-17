from django.utils import timezone
from django.contrib import messages
from django.contrib.sessions.models import Session
from .forms import WeekSelectForm
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, time
from django.contrib.auth.hashers import make_password, check_password
import ast


# 標頭
def header(request):
    username = request.session.get('username')
    username2 = Student.objects.get(studentID=username)
    return render(request, "base.html", locals())

# 登入

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # 先在 Student 模型中查找
        try:
            student = Student.objects.get(studentID=username)
            if check_password(password, student.password):
                request.session['username'] = student.studentID
                request.session['position'] = 'student'
                return redirect("/index", locals())
        except Student.DoesNotExist:
            pass

        # 再到 Teacher 模型中查找
        try:
            teacher = Teacher.objects.get(teacher_key=username)
            if check_password(password, teacher.password):
                request.session['username'] = teacher.teacher_key
                request.session['position'] = 'teacher'
                return redirect("/index", locals())
        except Teacher.DoesNotExist:
            pass

        message = '登入失敗！'

    return render(request, "login.html", locals())

# 更改密碼


def change_password(request):
    username = request.session.get('username')
    position = request.session.get('position')
    if position == 'student':
        username2 = Student.objects.get(studentID=username)
    else:
        username2 = Teacher.objects.get(teacher_key=username)
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if not check_password(current_password, username2.password):
            messages.error(request, '現有密碼不正確')
            return redirect('change_password')

        # 驗證新密碼和確認密碼是否匹配
        if new_password != confirm_password:
            messages.error(request, '新密碼和確認密碼不匹配')
            return redirect('change_password')

        # 使用 make_password 函數生成哈希並保存到數據庫
        username2.password = new_password
        username2.save()
        print("password", username2.password)
        messages.success(request, '密碼已成功更改')
        return redirect('change_password')

    return render(request, 'change_password.html', {
        "username2": username2,
    })
# 首頁


def index(request):
    username = request.session.get('username')
    position = request.session.get('position')
    print(username)
    print(position)
    if position == 'student':
        course_selection = Course_Selection.objects.filter(studentID=username)
        username2 = Student.objects.get(studentID=username)
    else:
        course = Course.objects.filter(teacher_key=username)
        username2 = Teacher.objects.get(teacher_key=username)
        print(type(username2))

    return render(request, "index.html", locals())

# 輸出樣板


def render_course_template(request, subject, seat_dict, course, course_seat, username2, msg=None, seats_per_column=None, classroom=None, position=None, students=None):
    return render(request, 'course.html', {
        "subject": subject,
        "seat": seat_dict,
        "course": course,
        "course_seat": course_seat,
        "username2": username2,
        "message": msg,
        "seats_per_column": seats_per_column,
        "classroom": classroom,
        "position": position,
        "students": students,
    })


# 計算星期
def calculate_week_number(current_time):
    # 添加第一周的起始時間
    first_week_start_time = datetime(2023, 9, 10)
    # 計算目前是第幾周
    weeks_passed = (current_time - first_week_start_time).days // 7 + 1

    return weeks_passed

# 課程


def course(request, subject):
    username = request.session.get('username')
    position = request.session.get('position')
    # 取得當前日期時間
    current_time = datetime.now()
    if position == 'student':
        course_selection = Course_Selection.objects.filter(studentID=username)
        username2 = Student.objects.get(studentID=username)
    else:
        course = Course.objects.filter(teacher_key=username)
        username2 = Teacher.objects.get(teacher_key=username)

    seats_per_column = [57, 54, 50, 40, 30, 20, 10]
    print('username:', username2)
    print(subject)

    try:
        course = Course.objects.get(course_name=subject)
        courses = Course.objects.filter(course_name=subject)
        students = Course_Selection.objects.filter(
            course_key=course).values_list('studentID__studentID', 'studentID__name')
        print('學生:', students)
        classroom = course.classroom.classroom_key
        print('classroom:', classroom, type(classroom))
        print(course)
        print(courses.values_list()[0][0])
        cid = courses.values_list()[0][0]
        msg = "None"

        # 計算現在第幾周
        weeks_passed = calculate_week_number(current_time)
        print(weeks_passed)

        try:
            course_seat = Course_seat.objects.filter(
                course_id=cid, week_number=weeks_passed)
            print(course_seat)
        except Exception as e:
            print(e)

        # 座位排列
        seat_dict = {}
        username_dict = {}
        for i in range(1, course.classroom.seat + 1):
            seat_dict[str(i)] = 0
        for i in course_seat:
            seat_dict[str(i.number)] = i.student

        # 獲取當前周數
        # 取得模型中的星期資訊
        week = course.day_of_week
        print("星期:", week)
        # 使用strftime函式將日期轉換為星期幾的數字（1到7）
        current_day_of_week = current_time.weekday() + 1
        week_same = week == current_day_of_week
        print(week_same)
        if week_same == True:
            # 選位時間
            class_datetime = datetime.combine(
                datetime.today(), course.class_time)
            if position != 'teacher':
                if not (class_datetime - timedelta(minutes=10) < current_time < class_datetime + timedelta(minutes=10)):
                    msg = "選位時間未到/已過"
                    return render_course_template(request, subject, seat_dict, course, course_seat, username2, msg, seats_per_column, classroom, position, students)
        else:
            msg = "今天沒有這堂課"
            return render_course_template(request, subject, seat_dict, course, course_seat, username2, msg, seats_per_column, classroom, position, students)
    except Course.DoesNotExist:
        return render(request, "course_not_found.html", {"subject": subject})

    if request.method == "POST":
        if position == 'teacher':
            selected_student = request.POST.get('selected_student')#包含元组的字符串
            # 解析字符串为元组
            selected_student_tuple = ast.literal_eval(selected_student)
            # 获取学生ID
            student_id = selected_student_tuple[0]
            selected_student = get_object_or_404(Student, studentID=student_id)
            # print(selected_student)
        try:
            number = request.POST['number']
        except:
            msg = "tt"
            return render_course_template(request, subject, seat_dict, course, course_seat, username2, msg, seats_per_column, classroom, position, students)
        if number is not None:
            print(number, course, username2)
            course2 = Course.objects.get(course_name=course)
            print(course)
            if position == 'teacher':
                check = Course_seat.objects.filter(
                    student=selected_student,
                    number__gt=0,
                    course=course2,
                    week_number=weeks_passed,
                )
            else:
                check = Course_seat.objects.filter(
                    student=username2,
                    number__gt=0,
                    course=course2,
                    week_number=weeks_passed,
                )
            if check:
                msg = "alert"
                print("以選位")
                return render_course_template(request, subject, seat_dict, course, course_seat, username2, msg, seats_per_column, classroom, position, students)
            else:
                if position == 'teacher':
                    seat, created = Course_seat.objects.update_or_create(
                        student=selected_student,
                        course=course2,
                        week_number=weeks_passed,
                        defaults={
                            'number': int(number),
                            'selection_time': current_time,
                            'is_absent': False,
                        }
                    )
                else:
                    seat, created = Course_seat.objects.update_or_create(
                        student=username2,
                        course=course2,
                        week_number=weeks_passed,
                        defaults={
                            'number': int(number),
                            'selection_time': current_time,
                            'is_absent': False,
                        }
                    )
                return redirect('course', subject=subject)
        else:
            msg = "alert"
            return render_course_template(request, subject, seat_dict, course, course_seat, username2, msg, seats_per_column, classroom, position, students)

    return render_course_template(request, subject, seat_dict, course, course_seat, username2, msg, seats_per_column, classroom, position, students)


# 缺曠


def record(request, subject):
    username = request.session.get('username')
    position = request.session.get('position')

    current_time = datetime.now()
    weeks_passed = calculate_week_number(current_time)

    all_weeks = range(1, 19)  
    form = WeekSelectForm(request.GET or None)
    selected_week = form['week_number'].value() if form.is_valid(
    ) and form['week_number'].value() != '' else None
    if selected_week == '':
        selected_week = None

    if position == 'student':
        course_selection = Course_Selection.objects.filter(studentID=username)
        username2 = Student.objects.get(studentID=username)
        course_seats = Course_seat.objects.filter(student=username)
    else:
        course = Course.objects.filter(teacher_key=username)
        username2 = Teacher.objects.get(teacher_key=username)
        if selected_week is not None:
            course_seats = Course_seat.objects.filter(
                week_number=selected_week, course__course_name=subject)
        else:
            course_seats = Course_seat.objects.filter(
                course__course_name=subject)
        print('course_seats', course_seats)

    del_btn = False  # 預設情況下不顯示刪除按鈕
    current_time_minus_10_minutes = current_time - timedelta(minutes=10)
    course_time = Course.objects.get(course_name=subject)
    class_datetime = datetime.combine(datetime.today(), course_time.class_time)
    course_time_start = class_datetime - timedelta(minutes=10)
    course_time_end = class_datetime + timedelta(minutes=10)

    # 學生缺曠補齊
    if position == 'teacher':
        course_name = get_object_or_404(Course, course_name=subject)
        selected_students = Course_Selection.objects.filter(
            course_key=course_name)
        course_seats_week = Course_seat.objects.filter(
            course=course_name,
            week_number=weeks_passed
        )
        # 遍歷選課學生，如果沒有出席記錄則創建記錄
        for student in selected_students:
            # 檢查該學生是否已經有出席記錄
            existing_record = course_seats_week.filter(
                student=student.studentID).first()

            if not existing_record:
                # 創建出席記錄
                Course_seat.objects.create(
                    student=student.studentID,
                    number=0,
                    course=course_name,
                    is_absent=True,
                    selection_time=current_time,
                    week_number=weeks_passed
                )

    if request.method == 'POST':
        course_seat_id = request.POST.get('course_seat_id')
        try:
            course_seat = Course_seat.objects.get(id=course_seat_id)
            course_seat.delete()
            messages.success(request, '成功刪除出席紀錄')
        except Course_seat.DoesNotExist:
            messages.error(request, '出席紀錄不存在')
        return redirect('record', subject=subject)

    print(username)
    print(course_seats)
    return render(request, "record.html", {
        "subject": subject,
        "position": position,
        'course_seats': course_seats,
        "username2": username2,
        "del_btn": del_btn,
        "current_time": current_time,
        'current_time_minus_10_minutes': current_time_minus_10_minutes,
        'course_time_start': course_time_start,
        'course_time_end': course_time_end,
        "form": form,
        "all_weeks": all_weeks,
        "selected_week": selected_week,

    })

# 登出
def logout(request):
    if 'username' in request.session:
        Session.objects.all().delete()
        return redirect('/login/')

    return redirect('/login/')

