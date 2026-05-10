from django.urls import path

from apps.learning import views_teacher
from . import views, views_theory, views_quiz

app_name = 'learning'

urlpatterns = [
    path('catalog/', views.catalog_view, name='catalog'),
    path('subject/<int:subject_id>/', views.subject_detail_view, name='subject_detail'),
    path('lesson/<int:lesson_id>/theory/', views_theory.theory_detail_view, name='theory'),
    path('lesson/<int:lesson_id>/quiz/', views_quiz.quiz_detail_view, name='quiz'),
    path('pomodoro/', views.pomodoro_view, name='pomodoro'),
    path('api/update-pomodoro-xp/', views.update_pomodoro_xp, name='update_pomodoro_xp'),
    path('teacher/', views_teacher.dashboard_view, name='teacher_dashboard'),
    path('teacher/', views_teacher.dashboard_view, name='teacher_dashboard'),
    path('teacher/lesson/add/', views_teacher.lesson_create_view, name='teacher_lesson_add'),
    path('teacher/quiz/add/', views_teacher.quiz_create_view, name='teacher_quiz_add'),
    path('teacher/map/add/', views_teacher.map_create_view, name='teacher_map_add'),
    path('teacher/flashcard/add/', views_teacher.flashcard_create_view, name='teacher_flashcard_add'),
]