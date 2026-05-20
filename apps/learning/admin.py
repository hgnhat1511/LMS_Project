from django.contrib import admin
from .models import Grade, ClassRoom, Subject, Lesson, QuizQuestion, QuizChoice, Flashcard

# Đăng ký bảng Khối Lớp
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

# Đăng ký bảng Lớp Học
@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade')
    list_filter = ('grade',) # Hiển thị bộ lọc theo khối bên phải

# Đăng ký nhanh các bảng khác để sau này dễ quản lý
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(QuizQuestion)
admin.site.register(QuizChoice)
admin.site.register(Flashcard)