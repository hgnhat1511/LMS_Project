from django.shortcuts import render, get_object_or_404
from apps.learning.models import Lesson
from .models import MapQuestion
import math


def map_quiz_view(request, lesson_id):
    # Lấy bài học ra
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Lấy câu hỏi bản đồ đầu tiên (nếu có)
    question = lesson.map_questions.first()
    
    return render(request, 'gis_maps/map_quiz.html', {
        'lesson': lesson,
        'question': question
    })


# Hàm tính khoảng cách đường chim bay (Thuật toán Haversine) trả về Mét
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000 # Bán kính Trái Đất (mét)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c 

def map_quiz_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    question = lesson.map_questions.first()
    
    context = {
        'lesson': lesson,
        'question': question,
        'is_submitted': False
    }

    # Nếu người dùng bấm Chốt Tọa độ
    if request.method == 'POST' and question:
        user_lat = request.POST.get('lat')
        user_lng = request.POST.get('lng')
        
        if user_lat and user_lng:
            # Lấy tọa độ mục tiêu từ Database
            target_lng = question.target_point.x
            target_lat = question.target_point.y
            
            # Tính toán khoảng cách (mét)
            distance_meters = calculate_distance(float(user_lat), float(user_lng), target_lat, target_lng)
            
            # Kiểm tra xem có nằm trong bán kính sai số cho phép không
            is_correct = distance_meters <= question.tolerance_radius
            
            # Đẩy kết quả ra màn hình
            context.update({
                'is_submitted': True,
                'is_correct': is_correct,
                'distance_km': round(distance_meters / 1000, 1),
                'max_km': round(question.tolerance_radius / 1000, 1)
            })

# Kiểm tra xem có nằm trong bán kính sai số cho phép không
            is_correct = distance_meters <= question.tolerance_radius
            
            xp_earned = 0
            if is_correct and request.user.is_authenticated:
                xp_earned = 30 # Chọn đúng bản đồ được thưởng tận 30 XP!
                request.user.profile.add_xp(xp_earned)
            
            # Đẩy kết quả ra màn hình
            context.update({
                'is_submitted': True,
                'is_correct': is_correct,
                'distance_km': round(distance_meters / 1000, 1),
                'max_km': round(question.tolerance_radius / 1000, 1),
                'xp_earned': xp_earned # Gửi ra frontend để hiện dòng chữ "+30 XP"
            })

    return render(request, 'gis_maps/map_quiz.html', context)