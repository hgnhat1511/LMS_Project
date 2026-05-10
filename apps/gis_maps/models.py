from django.contrib.gis.db import models # Chú ý: import models của GIS
from apps.learning.models import Lesson

class MapQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='map_questions', verbose_name="Bài học GIS")
    question_text = models.CharField(max_length=255, verbose_name="Câu hỏi (VD: Click vào tỉnh Nghệ An, Click vào vị trí Dinh Độc Lập)")
    
    # TRƯỜNG KHÔNG GIAN (SPATIAL FIELDS) của PostGIS
    # srid=4326 là hệ tọa độ chuẩn WGS84 (Giống Google Maps)
    
    # 1. Dùng cho câu hỏi tìm Vùng (Ví dụ: Tỉnh/Thành phố/Quốc gia)
    target_polygon = models.PolygonField(srid=4326, null=True, blank=True, verbose_name="Vùng đáp án đúng")
    
    # 2. Dùng cho câu hỏi tìm Điểm (Ví dụ: Tọa độ 1 di tích lịch sử cụ thể)
    target_point = models.PointField(srid=4326, null=True, blank=True, verbose_name="Tọa độ đúng")
    
    # Bán kính cho phép sai số (Tính bằng mét) nếu học sinh click vào điểm
    tolerance_radius = models.FloatField(default=5000, verbose_name="Sai số cho phép (mét)")

    def __str__(self):
        return f"Map Quiz: {self.question_text}"