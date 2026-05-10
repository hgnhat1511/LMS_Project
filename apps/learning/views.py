from django.shortcuts import render
from .models import Grade

# View hiển thị danh sách Khối lớp -> Môn học
def catalog_view(request):
    # Lấy tất cả Khối lớp, và lấy kèm luôn các Môn học thuộc khối đó (để tối ưu câu query SQL)
    grades = Grade.objects.prefetch_related('subjects').all()
    
    return render(request, 'learning/catalog.html', {'grades': grades})

from django.shortcuts import render, get_object_or_404
from .models import Grade, Subject

def catalog_view(request):
    grades = Grade.objects.prefetch_related('subjects').all()
    return render(request, 'learning/catalog.html', {'grades': grades})

# THÊM HÀM NÀY: Xem chi tiết môn học (hiển thị danh sách bài học)
def subject_detail_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    lessons = subject.lessons.all()
    return render(request, 'learning/subject_detail.html', {
        'subject': subject,
        'lessons': lessons
    })

# THÊM HÀM NÀY: Xử lý trang hiển thị Đồng hồ Pomodoro
def pomodoro_view(request):
    return render(request, 'learning/pomodoro.html')

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# API Xử lý cộng/trừ điểm Pomodoro
@login_required
def update_pomodoro_xp(request):
    if request.method == 'POST':
        try:
            # Lấy dữ liệu JS gửi lên
            data = json.loads(request.body)
            action = data.get('action')
            
            profile = request.user.profile
            
            if action == 'success':
                profile.add_xp(50) # Thưởng 50 XP
            elif action == 'fail':
                profile.add_xp(-20) # Phạt trừ 20 XP
                
                # Ép luật: Không cho phép XP rơi xuống âm
                if profile.total_xp < 0:
                    profile.total_xp = 0
                    profile.tree_level = 1
                    profile.save()
                    
            return JsonResponse({
                'status': 'ok', 
                'new_xp': profile.total_xp,
                'new_level': profile.tree_level
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'invalid request'})