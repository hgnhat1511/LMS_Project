from django.shortcuts import render, get_object_or_404
from .models import Lesson

def theory_detail_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Lấy toàn bộ thẻ Flashcard của bài học này
    flashcards = lesson.flashcards.all()
    
    if lesson.is_gis_map:
        pass
        
    return render(request, 'learning/theory.html', {
        'lesson': lesson,
        'flashcards': flashcards  # Truyền flashcards ra template
    })