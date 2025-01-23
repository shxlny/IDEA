from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True, null=True)  # Поле для никнейма
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Поле для аватара

    def __str__(self):
        return self.nickname or self.user.username  # Возвращает nickname, если он есть, иначе username

class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')  # Связь с пользователем
    title = models.CharField(max_length=255)  # Название идеи
    description = models.TextField()  # Описание идеи
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return self.title
