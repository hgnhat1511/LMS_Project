import math
from django.db import models
from apps.accounts.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class PlayerProgress(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='progress')
    
    # Tổng XP dùng để đua Top Bảng xếp hạng
    total_xp = models.IntegerField(default=0)
    
    # Thanh XP của riêng cấp độ hiện tại (Để vẽ thanh kinh nghiệm)
    current_level_xp = models.IntegerField(default=0)
    
    # Cấp độ hiện tại (Vô hạn)
    tree_level = models.IntegerField(default=1) 

    def __str__(self):
        return f"Tiến trình của {self.user.username} - Cấp {self.tree_level} ({self.total_xp} XP)"

    def xp_required(self):
        """
        CÔNG THỨC LEVEL MỚI: Cấp số nhân (Hàm mũ 1.5)
        Ví dụ: Cấp 1 cần 100 XP, Cấp 10 cần 3162 XP...
        """
        return int(100 * (self.tree_level ** 1.5))

    def add_xp(self, amount):
        """Logic tự động tính toán cấp độ cây (Cộng dồn và nhảy cấp vô hạn)"""
        if amount <= 0: return
        
        self.total_xp += amount
        self.current_level_xp += amount
        
        # Vòng lặp Level Up (Chạy liên tục nếu lượng XP nhận được đủ lên nhiều cấp)
        while self.current_level_xp >= self.xp_required():
            self.current_level_xp -= self.xp_required() # Giữ lại XP dư
            self.tree_level += 1
            
            # --- SỰ KIỆN ENDGAME 100+ ---
            # Mỗi 10 cấp chẵn (100, 120): Ra hoa
            # Mỗi 10 cấp lẻ (110, 130): Kết trái (Thưởng nóng lượng lớn XP)
            tier = self.tree_level // 10
            if self.tree_level >= 100 and self.tree_level % 10 == 0:
                if tier % 2 != 0: # Kết trái
                    fruit_bonus_xp = self.xp_required() 
                    self.total_xp += fruit_bonus_xp
                    self.current_level_xp += fruit_bonus_xp
                    
        self.save()

    def calculate_quiz_xp(self, correct_answers, total_questions):
        """
        - Đúng 1 câu = 50 XP. Cứ qua 10 cấp được tăng thêm 30 XP/câu.
        - Sai = Không trừ.
        - Trả lời đúng tất cả = Thưởng nóng 50 XP (Tăng 50 XP mỗi 10 cấp).
        """
        tier = self.tree_level // 10
        
        xp_per_question = 50 + (tier * 30)
        earned_xp = correct_answers * xp_per_question
        
        if total_questions > 0 and correct_answers == total_questions:
            perfect_bonus = 50 + (tier * 50)
            earned_xp += perfect_bonus
            
        return earned_xp

    def get_tree_stage_display(self):
        """Tên gọi hiển thị theo chặng (Mỗi 10 cấp tiến hóa 1 lần)"""
        lvl = self.tree_level
        if lvl < 10: return "Hạt mầm"
        if lvl < 20: return "Mầm non"
        if lvl < 30: return "Cây non đâm chồi"
        if lvl < 40: return "Cây tơ"
        if lvl < 50: return "Cây trưởng thành"
        if lvl < 60: return "Cây xum xuê"
        if lvl < 70: return "Cây cổ thụ"
        if lvl < 80: return "Cây tinh linh"
        if lvl < 90: return "Cây sinh mệnh"
        if lvl < 100: return "Cây thế giới"
        
        tier = lvl // 10
        if tier % 2 == 0:
            return f"Thần Thụ (Đang ra hoa 🌸) - Lv.{lvl}"
        else:
            return f"Thần Thụ (Đang kết trái 🍎) - Lv.{lvl}"

    def get_progress_percentage(self):
        """Trả về phần trăm (0-100) để làm UI thanh màu xanh"""
        return int((self.current_level_xp / self.xp_required()) * 100)


# =========================================================
# SIGNALS - GIỮ NGUYÊN HOÀN TOÀN CỦA BẠN
# =========================================================

# Tự động tạo PlayerProgress mỗi khi có User mới
@receiver(post_save, sender=CustomUser)
def create_player_progress(sender, instance, created, **kwargs):
    if created:
        PlayerProgress.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_player_progress(sender, instance, **kwargs):
    if hasattr(instance, 'progress'):
        instance.progress.save()