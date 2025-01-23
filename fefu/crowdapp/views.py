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
from .models import Idea


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']  # Убираем удалённые поля
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class NicknameChangeForm(forms.Form):
    nickname = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter new nickname',
            'class': 'form-control'
        })
    )

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

# Account view: профайл + изменение никнейма
@login_required
def account_view(request):
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        profile = Profile.objects.create(user=request.user)

    # Инициализация форм
    nickname_form = NicknameChangeForm(initial={'nickname': request.user.username})
    profile_form = ProfileForm(instance=profile)

    if request.method == 'POST':
        if 'avatar' in request.FILES:
            # Обработка изменения аватарки
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Avatar updated successfully!")
                return redirect('account')
        elif 'nickname' in request.POST:
            # Обработка изменения никнейма
            nickname_form = NicknameChangeForm(request.POST)
            if nickname_form.is_valid():
                new_nickname = nickname_form.cleaned_data['nickname']
                request.user.username = new_nickname
                request.user.save()
                messages.success(request, "Nickname updated successfully!")
                return redirect('account')

    # Возвращаем формы в шаблон
    return render(request, 'account.html', {
        'nickname_form': nickname_form,
        'profile_form': profile_form,
        'nickname': profile.nickname,
    })

@login_required
def add_idea(request):
    if request.method == 'POST':
        print("POST request received")  # Отладка
        title = request.POST.get('idea_title')
        description = request.POST.get('idea_desc')

        print(f"Title: {title}, Description: {description}")  # Проверка полученных данных

        if not title or not description:
            messages.error(request, "Both title and description are required!")
        else:
            Idea.objects.create(
                user=request.user,
                title=title,
                description=description
            )
            print("Idea saved successfully")  # Проверка сохранения
            messages.success(request, "Your idea has been published!")
            return redirect('account')

    return render(request, 'account.html')

from django.shortcuts import render
from .models import Idea

def main_page(request):
    ideas = Idea.objects.all()  # Получаем все идеи
    return render(request, 'main.html', {'ideas': ideas})
