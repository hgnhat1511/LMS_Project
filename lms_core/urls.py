from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls')),
    path('accounts/', include('apps.accounts.urls')),     # Gom các link đăng nhập, hồ sơ vào đây
    path('learning/', include('apps.learning.urls')),
    path('gis/', include('apps.gis_maps.urls')),
    path('gamification/', include('apps.gamification.urls')),
]