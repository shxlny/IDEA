from django import forms
from django.contrib.auth.models import User
from .models import Idea

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        })
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat password',
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Nickname',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        # Проверка на совпадение паролей
        if password != repeat_password:
            raise forms.ValidationError({
                'repeat_password': "Passwords do not match"
            })

        return cleaned_data

# Форма для изменения никнейма
class NicknameChangeForm(forms.Form):
    nickname = forms.CharField(
        max_length=100,
        required=True,
        label="New Nickname",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter new nickname',
            'class': 'form-control'
        })
    )

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter idea title',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter your description',
                'class': 'form-control'
            }),
        }
