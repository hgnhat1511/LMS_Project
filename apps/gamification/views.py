from django.shortcuts import render
from .models import PlayerProgress

def leaderboard_view(request):
    # Lấy top 10 người từ bảng PlayerProgress, sắp xếp điểm từ cao xuống thấp
    top_profiles = PlayerProgress.objects.select_related('user').order_by('-total_xp')[:10]
    
    return render(request, 'gamification/leaderboard.html', {'top_profiles': top_profiles})