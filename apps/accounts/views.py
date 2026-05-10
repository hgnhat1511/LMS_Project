from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm

# 1. Xử lý Trang chủ
def home_view(request):
    return render(request, 'layouts/base.html')

# 2. Xử lý Đăng ký
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# 3. Xử lý Đăng nhập (Đây chính là hàm hệ thống đang báo thiếu)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# 4. Xử lý Đăng xuất
def logout_view(request):
    logout(request)
    return redirect('accounts:home')

from django.contrib.auth.decorators import login_required
from .models import Profile

# 5. Xem Hồ sơ cá nhân & Cây Trí Tuệ
@login_required
def profile_view(request):
    # Dùng get_or_create để phòng hờ User chưa có Profile thì hệ thống tự tạo luôn
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

# 6. Bảng Xếp Hạng (Đua Top XP)
def leaderboard_view(request):
    # Lấy top 10 người có điểm XP cao nhất
    top_profiles = Profile.objects.select_related('user').order_by('-total_xp')[:10]
    return render(request, 'accounts/leaderboard.html', {'top_profiles': top_profiles})