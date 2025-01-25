from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django import forms
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Profile, Idea, IdeaVote, Comment
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Модели и формы
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']  #
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

# Регистрация пользователя (HTML)
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

# Авторизация пользователя (HTML)
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

    nickname_form = NicknameChangeForm(initial={'nickname': request.user.username})
    profile_form = ProfileForm(instance=profile)

    if request.method == 'POST':
        if 'avatar' in request.FILES:
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Avatar updated successfully!")
                return redirect('account')
        elif 'nickname' in request.POST:
            nickname_form = NicknameChangeForm(request.POST)
            if nickname_form.is_valid():
                new_nickname = nickname_form.cleaned_data['nickname']
                request.user.username = new_nickname
                request.user.save()
                messages.success(request, "Nickname updated successfully!")
                return redirect('account')

    return render(request, 'account.html', {
        'nickname_form': nickname_form,
        'profile_form': profile_form,
        'nickname': profile.nickname,
    })

@login_required
def add_idea(request):
    if request.method == 'POST':
        title = request.POST.get('idea_title')
        description = request.POST.get('idea_desc')
        category = request.POST.get('idea_category')

        if not title or not description or not category:
            messages.error(request, "All fields are required!")
            return redirect('account')

        Idea.objects.create(
            title=title,
            description=description,
            category=category,
            user=request.user
        )
        messages.success(request, "Your idea has been published!")
        return redirect('main')

    return redirect('account')

# Лайк идеи
def like_idea(request, idea_id):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            idea = get_object_or_404(Idea, id=idea_id)
            vote, created = IdeaVote.objects.get_or_create(user=request.user, idea=idea)

            if vote.vote_type == 'like':
                return JsonResponse({"success": False, "error": "You already liked this idea."})

            vote.vote_type = 'like'
            vote.save()

            idea.likes = IdeaVote.objects.filter(idea=idea, vote_type='like').count()
            idea.dislikes = IdeaVote.objects.filter(idea=idea, vote_type='dislike').count()
            idea.save()

            return JsonResponse({"success": True, "likes": idea.likes, "dislikes": idea.dislikes})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request or not authenticated."})

# Дизлайк идеи
def dislike_idea(request, idea_id):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            idea = get_object_or_404(Idea, id=idea_id)
            vote, created = IdeaVote.objects.get_or_create(user=request.user, idea=idea)

            if vote.vote_type == 'dislike':
                return JsonResponse({"success": False, "error": "You already disliked this idea."})

            vote.vote_type = 'dislike'
            vote.save()

            idea.likes = IdeaVote.objects.filter(idea=idea, vote_type='like').count()
            idea.dislikes = IdeaVote.objects.filter(idea=idea, vote_type='dislike').count()
            idea.save()

            return JsonResponse({"success": True, "likes": idea.likes, "dislikes": idea.dislikes})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request or not authenticated."})

# Комментарии к идее
def idea_comments(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    comments = idea.comments.all()
    return render(request, 'idea_comments.html', {'idea': idea, 'comments': comments})

# Добавление комментария
@login_required
@require_POST
def add_comment(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    comment_text = request.POST.get('comment')

    if comment_text:
        if len(comment_text) > 100:
            messages.error(request, f"The comment cannot exceed 100 characters.")
            return redirect('idea_comments', idea_id=idea.id)

        Comment.objects.create(
            idea=idea,
            author=request.user,
            text=comment_text
        )

    return redirect('idea_comments', idea_id=idea.id)

# API-классы

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Idea, IdeaVote, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Регистрация пользователя
class UserSignupAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Register a new user",
        responses={201: openapi.Response('User created successfully')},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nickname': openapi.Schema(type=openapi.TYPE_STRING, description='User nickname'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
                'repeat_password': openapi.Schema(type=openapi.TYPE_STRING, description='Repeat user password'),
            }
        )
    )
    def post(self, request):
        nickname = request.data.get('nickname').strip()
        email = request.data.get('email').strip()
        password = request.data.get('password').strip()
        repeat_password = request.data.get('repeat_password').strip()

        if not nickname or not email or not password or not repeat_password:
            return Response({"error": "All fields are required!"}, status=status.HTTP_400_BAD_REQUEST)

        if password != repeat_password:
            return Response({"error": "Passwords do not match!"}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({"error": "Password must be at least 8 characters long!"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=nickname).exists():
            return Response({"error": "Nickname already taken!"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already in use!"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=nickname, email=email, password=password)
        user.save()
        return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)

# Авторизация пользователя
class UserLoginAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Authenticate a user",
        responses={200: openapi.Response('Successfully logged in'), 400: openapi.Response('Invalid credentials')},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nickname': openapi.Schema(type=openapi.TYPE_STRING, description='User nickname'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            }
        )
    )
    def post(self, request):
        username = request.data.get('nickname').strip()
        password = request.data.get('password').strip()

        if not username or not password:
            return Response({"error": "Both nickname and password are required!"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Successfully logged in!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid nickname or password!"}, status=status.HTTP_400_BAD_REQUEST)

# Добавление идеи
class AddIdeaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a new idea",
        responses={201: openapi.Response('Idea added successfully')},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'idea_title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the idea'),
                'idea_desc': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the idea'),
                'idea_category': openapi.Schema(type=openapi.TYPE_STRING, description='Category of the idea'),
            }
        )
    )
    def post(self, request):
        title = request.data.get('idea_title')
        description = request.data.get('idea_desc')
        category = request.data.get('idea_category')

        if not title or not description or not category:
            return Response({"error": "All fields are required!"}, status=status.HTTP_400_BAD_REQUEST)

        Idea.objects.create(
            title=title,
            description=description,
            category=category,
            user=request.user
        )
        return Response({"message": "Your idea has been published!"}, status=status.HTTP_201_CREATED)

# Лайк идеи
class LikeIdeaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Like an idea",
        responses={200: openapi.Response('Idea liked successfully'), 400: openapi.Response('You already liked this idea')},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={}
        )
    )
    def post(self, request, idea_id):
        idea = get_object_or_404(Idea, id=idea_id)
        vote, created = IdeaVote.objects.get_or_create(user=request.user, idea=idea)

        if vote.vote_type == 'like':
            return Response({"error": "You already liked this idea."}, status=status.HTTP_400_BAD_REQUEST)

        vote.vote_type = 'like'
        vote.save()

        idea.likes = IdeaVote.objects.filter(idea=idea, vote_type='like').count()
        idea.dislikes = IdeaVote.objects.filter(idea=idea, vote_type='dislike').count()
        idea.save()

        return Response({"success": True, "likes": idea.likes, "dislikes": idea.dislikes}, status=status.HTTP_200_OK)

# Добавление комментария
class AddCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a comment to an idea",
        responses={201: openapi.Response('Comment added successfully')},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Text of the comment'),
            }
        )
    )
    def post(self, request, idea_id):
        idea = get_object_or_404(Idea, id=idea_id)
        comment_text = request.data.get('comment')

        if len(comment_text) > 100:
            return Response({"error": "The comment cannot exceed 100 characters."}, status=status.HTTP_400_BAD_REQUEST)

        Comment.objects.create(
            idea=idea,
            author=request.user,
            text=comment_text
        )

        return Response({"message": "Comment added successfully!"}, status=status.HTTP_201_CREATED)


def main_page(request):
    category = request.GET.get('category')
    if category:
        ideas = Idea.objects.filter(category=category).order_by('-likes')
    else:
        ideas = Idea.objects.all().order_by('-likes')

    print(f"Retrieved ideas: {ideas}")  # Проверка, какие данные подгружаются
    return render(request, 'main.html', {'ideas': ideas})
