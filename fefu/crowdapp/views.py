from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django import forms
from .models import Profile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'idea_title', 'idea_desc']
        widgets = {
            'idea_title': forms.TextInput(attrs={
                'placeholder': 'Enter idea title',
                'class': 'form-control'
            }),
            'idea_desc': forms.Textarea(attrs={
                'placeholder': 'Enter idea description',
                'class': 'form-control'
            }),
        }
# Регистрация пользователя
def user_signup(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        repeat_password = request.POST.get('repeat_password').strip()

        if not nickname or not email or not password or not repeat_password:
            messages.error(request, "All fields are required!")
            return render(request, 'reg.html')

        if password != repeat_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'reg.html')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long!")
            return render(request, 'reg.html')

        if User.objects.filter(username=nickname).exists():
            messages.error(request, "Nickname already taken!")
            return render(request, 'reg.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return render(request, 'reg.html')

        try:
            user = User.objects.create_user(username=nickname, email=email, password=password)
            user.save()
            Profile.objects.create(user=user, nickname=nickname)  # Создание профиля с никнеймом
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        except Exception as e:
            print(f"Error creating user: {e}")
            messages.error(request, "An error occurred while creating your account. Please try again.")
            return render(request, 'reg.html')

    return render(request, 'reg.html')

# Авторизация пользователя
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('nickname').strip()
        password = request.POST.get('password').strip()

        if not username or not password:
            messages.error(request, "Both nickname and password are required!")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('main')
        else:
            messages.error(request, "Invalid nickname or password!")
            return render(request, 'login.html')

    return render(request, 'login.html')

# Главная страница
def main_page(request):
    return render(request, 'main.html')

# Страница новостей
def news_page(request):
    return render(request, 'news.html')

# О проекте
def about_page(request):
    return render(request, 'about.html')

# FAQ
def faq_page(request):
    return render(request, 'faq.html')

# Обновление фото профиля
@login_required
@csrf_exempt
def update_photo(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        profile.avatar = request.FILES['photo']
        profile.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def change_nickname(request):
    try:
        profile = request.user.profile  # Получаем профиль текущего пользователя
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('profile')  # Перенаправляем на страницу профиля
    else:
        form = ChangeNicknameForm(instance=profile)

    return render(request, 'profile/change_nickname.html', {'form': form})

# Обновление профиля (включает никнейм и фото)
@login_required
def update_profile(request):
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        profile = Profile.objects.create(user=request.user)

    # Если форма отправлена (POST запрос)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('account')
    else:
        # Если форма не отправлена, то передаем форму для отображения
        form = ProfileForm(instance=profile)

    return render(request, 'account.html', {
        'form': form,
        'nickname': profile.nickname,  # Передаем никнейм в шаблон
    })


def add_idea(request):
    if request.method == 'POST':
        idea_title = request.POST.get('idea_title')  # Получаем данные из формы
        idea_desc = request.POST.get('idea_desc')

        # Получаем профиль текущего пользователя
        profile = request.user.profile

        # Если профиль существует, сохраняем идею
        if profile:
            profile.idea_title = idea_title
            profile.idea_desc = idea_desc
            profile.save()  # Сохраняем изменения в базе данных

            return redirect('profile')  # Перенаправляем на страницу профиля или куда-то еще

    return render(request, 'account.html')

class ChangeNicknameForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname']
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter new nickname'
            })
        }