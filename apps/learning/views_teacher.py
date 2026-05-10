from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Subject, Lesson, QuizQuestion, QuizChoice
from apps.accounts.models import CustomUser
from .forms import FlashcardForm, LessonForm, QuizQuestionForm,MapQuestionForm
from django.contrib.gis.geos import Point

# ... (Các hàm cũ giữ nguyên) ...


# 1. Hàm rào chắn: Chỉ cho phép Giáo viên đi qua
def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'

# 2. Trang Tổng quan (Bảng điều khiển của Giáo viên)
@user_passes_test(is_teacher, login_url='/login/')
def dashboard_view(request):
    # Đếm số lượng dữ liệu để hiển thị ra bảng thống kê
    total_students = CustomUser.objects.filter(role='student').count()
    total_subjects = Subject.objects.count()
    total_lessons = Lesson.objects.count()
    
    return render(request, 'learning/teacher/dashboard.html', {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_lessons': total_lessons,
    })

# 3. Xử lý giao diện Soạn Bài học (Lý thuyết)
@user_passes_test(is_teacher, login_url='/login/')
def lesson_create_view(request):
    if request.method == 'POST':
        # Nếu giáo viên bấm nút "Lưu Bài Giảng"
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save() # Lưu thẳng vào Database
            return redirect('learning:teacher_dashboard') # Lưu xong quay về trang tổng quan
    else:
        # Nếu mới vào trang thì hiện form trống
        form = LessonForm()
        
    return render(request, 'learning/teacher/lesson_form.html', {'form': form})

# 4. Xử lý giao diện Tạo Trắc nghiệm (A, B, C, D)
@user_passes_test(is_teacher, login_url='/login/')
def quiz_create_view(request):
    if request.method == 'POST':
        form = QuizQuestionForm(request.POST)
        if form.is_valid():
            # 1. Tạo Câu hỏi
            question = QuizQuestion.objects.create(
                lesson=form.cleaned_data['lesson'],
                question_text=form.cleaned_data['question_text']
            )
            
            # 2. Tạo 4 đáp án và gài cờ đúng/sai
            correct_idx = form.cleaned_data['correct_choice']
            
            QuizChoice.objects.create(question=question, choice_text=form.cleaned_data['choice_1'], is_correct=(correct_idx == '1'))
            QuizChoice.objects.create(question=question, choice_text=form.cleaned_data['choice_2'], is_correct=(correct_idx == '2'))
            QuizChoice.objects.create(question=question, choice_text=form.cleaned_data['choice_3'], is_correct=(correct_idx == '3'))
            QuizChoice.objects.create(question=question, choice_text=form.cleaned_data['choice_4'], is_correct=(correct_idx == '4'))
            
            # Lưu xong, tải lại trang để nhập câu tiếp theo
            return redirect('learning:teacher_quiz_add')
    else:
        form = QuizQuestionForm()
        
    return render(request, 'learning/teacher/quiz_form.html', {'form': form})

# THÊM HÀM NÀY XUỐNG DƯỚI CÙNG
@user_passes_test(is_teacher, login_url='/login/')
def map_create_view(request):
    if request.method == 'POST':
        form = MapQuestionForm(request.POST)
        if form.is_valid():
            # Khoan lưu vội, lấy object ra để gán tọa độ đã
            map_question = form.save(commit=False)
            
            # Lấy lat, lng từ 2 trường ẩn
            lat = form.cleaned_data['lat']
            lng = form.cleaned_data['lng']
            
            # GEOS Point nhận tham số theo thứ tự (Kinh độ, Vĩ độ) = (X, Y)
            map_question.target_point = Point(lng, lat, srid=4326)
            
            # Lưu chính thức vào DB
            map_question.save()
            return redirect('learning:teacher_dashboard')
    else:
        form = MapQuestionForm(initial={'tolerance_radius': 15000}) # Mặc định sai số 15km
        
    return render(request, 'learning/teacher/map_form.html', {'form': form})


@user_passes_test(is_teacher, login_url='/login/')
def flashcard_create_view(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            form.save()
            # Lưu xong thì tải lại ngay trang này để giáo viên nhập liên tục từ vựng thứ 2, thứ 3...
            return redirect('learning:teacher_flashcard_add') 
    else:
        form = FlashcardForm()
        
    return render(request, 'learning/teacher/flashcard_form.html', {'form': form})