from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages # Import messages để hiển thị thông báo
from apps.learning.models import Lesson
from .models import MapQuestion
from apps.gamification.models import PlayerProgress
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000 
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c 

def map_quiz_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    question = lesson.map_questions.first()
    
    # 1. Kiểm tra xem trong Session có lưu kết quả bài làm trước đó không
    result_data = request.session.pop('map_quiz_result', None)

    context = {
        'lesson': lesson,
        'question': question,
        'is_submitted': result_data is not None,
    }

    # Nếu có kết quả trả về từ lượt POST trước, gán vào context để HTML hiển thị
    if result_data:
        context.update(result_data)

    # 2. Xử lý khi user gửi form Tọa độ
    if request.method == 'POST' and question:
        user_lat = request.POST.get('lat')
        user_lng = request.POST.get('lng')
        
        if user_lat and user_lng:
            target_lng = question.target_point.x
            target_lat = question.target_point.y
            
            distance_meters = calculate_distance(float(user_lat), float(user_lng), target_lat, target_lng)
            is_correct = distance_meters <= question.tolerance_radius
            
            xp_earned = 0
            # Cộng điểm nếu đúng
            if is_correct and request.user.is_authenticated:
                xp_earned = 30 
                progress, created = PlayerProgress.objects.get_or_create(user=request.user)
                progress.add_xp(xp_earned)
                
            # Lưu kết quả vào Session thay vì Render trực tiếp
            request.session['map_quiz_result'] = {
                'is_correct': is_correct,
                'distance_km': round(distance_meters / 1000, 1),
                'max_km': round(question.tolerance_radius / 1000, 1),
                'xp_earned': xp_earned
            }
            
            # PRG: Chuyển hướng lại chính trang này (chuyển POST thành GET)
            return redirect('gis_maps:map_quiz', lesson_id=lesson.id)

    return render(request, 'gis_maps/map_quiz.html', context)