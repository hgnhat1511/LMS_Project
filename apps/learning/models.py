from django.db import models

# 1. Khối lớp (Ví dụ: Khối 1, Khối 2...)
class Grade(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Tên Khối")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")

    def __str__(self):
        return self.name

# 2. Môn học (Ví dụ: Toán, Tiếng Việt, Lịch Sử & Địa Lý...)
class Subject(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects', verbose_name="Khối lớp")
    name = models.CharField(max_length=100, verbose_name="Tên Môn học")
    cover_image = models.ImageField(upload_to='subjects/', blank=True, null=True, verbose_name="Ảnh bìa")

    def __str__(self):
        return f"{self.name} - {self.grade.name}"

# 3. Bài học (Chứa phần LÝ THUYẾT)
class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons', verbose_name="Môn học")
    title = models.CharField(max_length=200, verbose_name="Tên Bài học")
    theory_content = models.TextField(verbose_name="Nội dung Lý thuyết (HTML)")
    order = models.PositiveIntegerField(default=1, verbose_name="Thứ tự bài học")
    
    # Đánh dấu bài này có phải là bài GIS Bản đồ không để sau này rẽ nhánh
    is_gis_map = models.BooleanField(default=False, verbose_name="Là bài học Bản đồ?")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Bài {self.order}: {self.title}"

# 4. Câu hỏi Trắc nghiệm thường (Phục vụ phần TRẮC NGHIỆM)
class QuizQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions', verbose_name="Bài học")
    question_text = models.TextField(verbose_name="Nội dung câu hỏi")
    
    def __str__(self):
        return f"Câu hỏi của: {self.lesson.title}"

# 5. Các lựa chọn đáp án cho Trắc nghiệm (A, B, C, D)
class QuizChoice(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200, verbose_name="Nội dung đáp án")
    is_correct = models.BooleanField(default=False, verbose_name="Là đáp án đúng?")

    def __str__(self):
        return self.choice_text
    
# 6. Thẻ ghi nhớ (Flashcard) dùng trong phần Lý thuyết
class Flashcard(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='flashcards', verbose_name="Bài học")
    front_text = models.CharField(max_length=255, verbose_name="Mặt trước (Thuật ngữ)")
    back_text = models.TextField(verbose_name="Mặt sau (Định nghĩa)")

    def __str__(self):
        return f"Flashcard: {self.front_text}"