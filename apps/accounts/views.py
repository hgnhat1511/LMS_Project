from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Profile
# IMPORT BẢNG XP TỪ GAMIFICATION
from apps.gamification.models import PlayerProgress

# 1. Xử lý Đăng ký
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard:home') # <-- ĐÃ SỬA
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# 2. Xử lý Đăng nhập
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:home') # <-- ĐÃ SỬA
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# 3. Xử lý Đăng xuất
def logout_view(request):
    logout(request)
    return redirect('dashboard:home') # <-- ĐÃ SỬA

# 4. Xem Hồ sơ cá nhân & Cây Trí Tuệ
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    # Lấy thêm dữ liệu từ Gamification để hiển thị Cây
    progress, created_prog = PlayerProgress.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'progress': progress
    })