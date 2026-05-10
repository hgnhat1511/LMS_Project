from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    # CHỈ liệt kê 2 quyền này ra form public
    ALLOWED_ROLES = (
        ('student', 'Học sinh'),
        ('teacher', 'Giáo viên'),
    )
    role = forms.ChoiceField(choices=ALLOWED_ROLES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']