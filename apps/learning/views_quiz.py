from django.shortcuts import render, redirect, get_object_or_404
from .models import Lesson, QuizChoice
# IMPORT BẢNG XP TỪ GAMIFICATION
from apps.gamification.models import PlayerProgress

def quiz_detail_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # BẺ LÁI: Nếu là bài bản đồ, ném thẳng sang app gis_maps
    if lesson.is_gis_map:
        return redirect('gis_maps:map_quiz', lesson_id=lesson.id)

    # Lấy danh sách câu hỏi kèm đáp án
    questions = lesson.questions.prefetch_related('choices').all()
    
    # Nếu học sinh nhấn nút "Nộp bài"
    if request.method == 'POST':
        score = 0
        total = questions.count()
        
        # Chấm điểm từng câu
        for q in questions:
            selected_choice_id = request.POST.get(f'question_{q.id}')
            if selected_choice_id:
                is_correct = QuizChoice.objects.filter(id=selected_choice_id, is_correct=True).exists()
                if is_correct:
                    score += 1
                    
        # LOGIC GAMIFICATION MỚI: Gọi hàm calculate_quiz_xp từ Model
        xp_earned = 0
        if request.user.is_authenticated:
            progress, created = PlayerProgress.objects.get_or_create(user=request.user)
            
            # Đưa số câu đúng (score) và tổng câu (total) vào để Model tự tính toán
            xp_earned = progress.calculate_quiz_xp(correct_answers=score, total_questions=total)
            progress.add_xp(xp_earned)
        
        # Trả về kết quả
        return render(request, 'learning/quiz.html', {
            'lesson': lesson, 
            'score': score, 
            'total': total,
            'percentage': round((score / total) * 100) if total > 0 else 0,
            'is_submitted': True,
            'xp_earned': xp_earned 
        })

    # Nếu chỉ mới vào trang (chưa nộp bài)
    return render(request, 'learning/quiz.html', {
        'lesson': lesson, 
        'questions': questions, 
        'is_submitted': False
    })