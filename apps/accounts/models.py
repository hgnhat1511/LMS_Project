from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. Bảng User Tùy chỉnh
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Học sinh'),
        ('teacher', 'Giáo viên'),
        ('admin', 'Quản trị viên'),
    )
    # Ghi đè role, mặc định ai đăng ký cũng là học sinh
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

# Mở file apps/accounts/models.py và sửa class Profile thành thế này:
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    total_xp = models.IntegerField(default=0)
    tree_level = models.IntegerField(default=1) # 1: Hạt mầm -> 5: Cổ thụ
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"Profile của {self.user.username} - Cấp {self.tree_level}"

    # THÊM HÀM NÀY: Logic tự động tính toán cấp độ cây khi được cộng XP
    def add_xp(self, xp_earned):
        self.total_xp += xp_earned
        # Luật tiến hóa: Cứ 50 XP thì lên 1 cấp. Tối đa cấp 5.
        # Bạn có thể tự đổi số 50 thành con số bạn muốn.
        new_level = (self.total_xp // 50) + 1 
        
        if new_level > 5:
            new_level = 5 # Khóa max level là 5
            
        self.tree_level = new_level
        self.save()

# 3. Tự động tạo Profile mỗi khi có một CustomUser mới được đăng ký
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()