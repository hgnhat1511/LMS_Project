from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Giữ lại tạm để check DB nếu cần
    path('', include('apps.accounts.urls')), # Trỏ trang chủ về app accounts
    path('learning/', include('apps.learning.urls')),
    path('gis/', include('apps.gis_maps.urls')),
]