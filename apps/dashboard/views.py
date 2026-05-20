from django.shortcuts import render

# Chịu trách nhiệm hiển thị mặt tiền của website
def home_view(request):
    # Trả về giao diện trang chủ
    return render(request, 'dashboard/home.html')