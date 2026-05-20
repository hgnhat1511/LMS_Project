import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Grade, Lesson, Subject
# IMPORT BẢNG XP TỪ GAMIFICATION
from apps.gamification.models import PlayerProgress

# View hiển thị danh sách Khối lớp -> Môn học
def catalog_view(request):
    grades = Grade.objects.prefetch_related('subjects').all()
    return render(request, 'learning/catalog.html', {'grades': grades})

# Xem chi tiết môn học (hiển thị danh sách bài học)
def subject_detail_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    lessons = subject.lessons.all()
    return render(request, 'learning/subject_detail.html', {
        'subject': subject,
        'lessons': lessons
    })

# Xử lý trang hiển thị Đồng hồ Pomodoro
def pomodoro_view(request):
    return render(request, 'learning/pomodoro.html')

# API Xử lý cộng/trừ điểm Pomodoro
@login_required
def update_pomodoro_xp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            progress, created = PlayerProgress.objects.get_or_create(user=request.user)
            
            if action == 'success':
                # SCALE THEO TIER: Cứ 10 cấp được cộng thêm 20 XP bonus
                tier = progress.tree_level // 10
                xp_reward = 50 + (tier * 20)
                progress.add_xp(xp_reward)
                
            elif action == 'fail':
                # ĐÃ SỬA: Trừ 20 điểm khi bỏ cuộc hoặc chuyển tab (Đảm bảo không bị số âm)
                progress.total_xp = max(0, progress.total_xp - 20)
                progress.save()
                    
            return JsonResponse({
                'status': 'ok', 
                'new_xp': progress.total_xp,
                'new_level': progress.tree_level
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'invalid request'})

# Thêm view này vào cuối file
def flashcard_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    flashcards = lesson.flashcards.all()
    
    return render(request, 'learning/flashcards.html', {
        'lesson': lesson,
        'flashcards': flashcards
    })