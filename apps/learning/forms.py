from django import forms

from apps.gis_maps.models import MapQuestion
from .models import Lesson, QuizQuestion, Flashcard

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        # Khai báo các trường giáo viên cần nhập
        fields = ['subject', 'title', 'order', 'theory_content', 'is_gis_map']
        
        # Thêm CSS class để giao diện đẹp hơn
        widgets = {
            'subject': forms.Select(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc;'}),
            'title': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc;', 'placeholder': 'VD: Bài 3: Số đếm đến 100'}),
            'order': forms.NumberInput(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc;'}),
            'theory_content': forms.Textarea(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; font-family: monospace;', 'rows': 8, 'placeholder': 'Viết nội dung lý thuyết (Có thể dùng thẻ HTML như <h2>, <b>, <p>)...'}),
            'is_gis_map': forms.CheckboxInput(attrs={'style': 'transform: scale(1.5); margin-left: 10px;'}),
        }
        labels = {
            'subject': 'Chọn môn học',
            'title': 'Tên bài học',
            'order': 'Thứ tự bài',
            'theory_content': 'Nội dung Lý thuyết',
            'is_gis_map': 'Đánh dấu đây là bài học Bản đồ GIS (Dành cho Lịch sử/Địa lý)'
        }

# THÊM VÀO CUỐI FILE forms.py
class QuizQuestionForm(forms.Form):
    # Chỉ lấy những bài học bình thường (không phải bài GIS)
    lesson = forms.ModelChoiceField(
        queryset=Lesson.objects.filter(is_gis_map=False), 
        label="Chọn Bài học",
        widget=forms.Select(attrs={'style': 'width: 100%; padding: 10px; border-radius: 4px;'})
    )
    question_text = forms.CharField(
        label="Nội dung câu hỏi", 
        widget=forms.Textarea(attrs={'style': 'width: 100%; padding: 10px; border-radius: 4px;', 'rows': 3})
    )
    
    # 4 Ô nhập đáp án
    choice_1 = forms.CharField(label="Đáp án A", widget=forms.TextInput(attrs={'style': 'width: 100%; padding: 8px;'}))
    choice_2 = forms.CharField(label="Đáp án B", widget=forms.TextInput(attrs={'style': 'width: 100%; padding: 8px;'}))
    choice_3 = forms.CharField(label="Đáp án C", widget=forms.TextInput(attrs={'style': 'width: 100%; padding: 8px;'}))
    choice_4 = forms.CharField(label="Đáp án D", widget=forms.TextInput(attrs={'style': 'width: 100%; padding: 8px;'}))
    
    # Chọn xem đáp án nào đúng
    CORRECT_CHOICES = [
        ('1', 'Đáp án A là đáp án đúng'),
        ('2', 'Đáp án B là đáp án đúng'),
        ('3', 'Đáp án C là đáp án đúng'),
        ('4', 'Đáp án D là đáp án đúng'),
    ]
    correct_choice = forms.ChoiceField(
        choices=CORRECT_CHOICES, 
        label="Chỉ định đáp án đúng",
        widget=forms.Select(attrs={'style': 'width: 100%; padding: 10px; background-color: #d4efdf; font-weight: bold;'})
    )

# THÊM CLASS NÀY XUỐNG CUỐI FILE
class MapQuestionForm(forms.ModelForm):
    # Chỉ hiển thị những bài học có cờ is_gis_map = True
    lesson = forms.ModelChoiceField(
        queryset=Lesson.objects.filter(is_gis_map=True), 
        label="Chọn Bài học Bản đồ",
        widget=forms.Select(attrs={'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #ccc;'})
    )
    
    # 2 trường ẩn để JS âm thầm điền tọa độ vào khi Giáo viên click bản đồ
    lat = forms.FloatField(widget=forms.HiddenInput(attrs={'id': 'input-lat'}))
    lng = forms.FloatField(widget=forms.HiddenInput(attrs={'id': 'input-lng'}))

    class Meta:
        model = MapQuestion
        fields = ['lesson', 'question_text', 'tolerance_radius']
        widgets = {
            'question_text': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #ccc;', 'placeholder': 'VD: Hãy xác định vị trí của Vịnh Hạ Long'}),
            'tolerance_radius': forms.NumberInput(attrs={'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #ccc;'}),
        }
        labels = {
            'question_text': 'Nhiệm vụ cho học sinh',
            'tolerance_radius': 'Bán kính sai số cho phép (Tính bằng mét - VD: 15000 là 15km)'
        }

class FlashcardForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(
        queryset=Lesson.objects.all(), 
        label="Chọn Bài học",
        widget=forms.Select(attrs={'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #ccc;'})
    )
    
    class Meta:
        model = Flashcard
        fields = ['lesson', 'front_text', 'back_text']
        widgets = {
            'front_text': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #ccc;', 'placeholder': 'VD: Apple, 1+1=?'}),
            'back_text': forms.Textarea(attrs={'style': 'width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #ccc;', 'rows': 4, 'placeholder': 'VD: Quả táo, Bằng 2...'}),
        }
        labels = {
            'front_text': 'Mặt trước (Thuật ngữ / Câu hỏi ngắn)',
            'back_text': 'Mặt sau (Định nghĩa / Đáp án)'
        }