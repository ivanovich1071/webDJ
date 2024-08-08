from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    telephon = forms.CharField(max_length=15, required=True, help_text='Телефон')

    class Meta:
        model = User
        fields = ('username', 'telephon', 'password1', 'password2')
