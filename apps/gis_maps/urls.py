from django.urls import path
from . import views

app_name = 'gis_maps' # Tên namespace mà Django đang phàn nàn là thiếu

urlpatterns = [
    # Đường dẫn sẽ trông giống như: /gis/lesson/28/map-quiz/
    path('lesson/<int:lesson_id>/map-quiz/', views.map_quiz_view, name='map_quiz'),
]