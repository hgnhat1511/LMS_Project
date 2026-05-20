import os
import json
import django

# --- CẤU HÌNH ĐỂ SCRIPT CHẠY ĐƯỢC MÔI TRƯỜNG DJANGO ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_core.settings') 
django.setup()

from apps.learning.models import Grade, Subject, Lesson, QuizQuestion, QuizChoice

def run_import():
    # 1. Tìm hoặc tạo Khối lớp (Vì Subject bắt buộc phải có Grade)
    grade, created = Grade.objects.get_or_create(
        name="Khối Tiếng Anh",
        defaults={'description': 'Khối dùng để ôn tập từ vựng'}
    )
    if created:
        print("✅ Đã tạo mới: Khối Tiếng Anh")

    # 2. Tìm hoặc tạo Môn học Tiếng Anh
    subject, created = Subject.objects.get_or_create(
        name="Môn Tiếng Anh",
        grade=grade  # Khớp với ForeignKey trong models.py
    )
    if created:
        print("✅ Đã tạo mới: Môn Tiếng Anh")

    # 3. Tìm hoặc tạo Bài học để chứa 440 câu hỏi
    lesson, created = Lesson.objects.get_or_create(
        subject=subject,
        title="Ôn tập 440 Từ Vựng Tiếng Anh",
        defaults={
            'order': 1,
            'theory_content': 'Đây là bài học tổng hợp 440 từ vựng Tiếng Anh trắc nghiệm.', # Bắt buộc phải có vì model của bạn yêu cầu
            'is_gis_map': False
        }
    )
    if created:
        print("✅ Đã tạo mới: Bài học Ôn tập 440 Từ Vựng Tiếng Anh")

    # 4. Đọc file HTML của bạn và trích xuất dữ liệu JSON
    file_path = 'Full_Vocabulary_Quiz_440_Words.html'
    
    if not os.path.exists(file_path):
        print(f"❌ Lỗi: Không tìm thấy file {file_path}. Hãy để file này cùng thư mục với script.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Tìm đoạn chứa dữ liệu JSON (const quizData = [...];)
        start_marker = "const quizData = "
        end_marker = "];"
        
        start_index = content.find(start_marker)
        if start_index == -1:
            print("❌ Lỗi: Không tìm thấy biến 'quizData' trong file HTML.")
            return
            
        start_index += len(start_marker)
        end_index = content.find(end_marker, start_index) + 1 # +1 để lấy dấu ']'
        
        json_data_str = content[start_index:end_index]
        
        # Chuyển đổi chuỗi thành danh sách Python
        quiz_data = json.loads(json_data_str)
        
        print(f"🚀 Bắt đầu import {len(quiz_data)} câu hỏi vào Database...")
        
        count = 0
        for item in quiz_data:
            # Tạo câu hỏi
            question = QuizQuestion.objects.create(
                lesson=lesson,
                question_text=item['question']
            )
            
            # Tạo 4 đáp án
            options = item['options']
            correct_index = int(item['answer'])
            
            for index, option_text in enumerate(options):
                QuizChoice.objects.create(
                    question=question,
                    choice_text=option_text,
                    is_correct=(index == correct_index)
                )
            count += 1
            if count % 50 == 0:
                print(f"  Đã import {count}/{len(quiz_data)} câu...")

        print(f"🎉 HOÀN THÀNH TỐT ĐẸP! Đã import thành công {count} câu hỏi vào bài học '{lesson.title}'.")

    except Exception as e:
        print(f"❌ Lỗi trong quá trình xử lý: {str(e)}")

if __name__ == '__main__':
    run_import()