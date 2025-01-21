from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True, null=True)  # Поле для никнейма
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Поле для аватара

    # Поля для идеи
    idea_title = models.CharField(max_length=255, blank=True, null=True)  # Название идеи
    idea_desc = models.TextField(blank=True, null=True)  # Описание идеи

    def __str__(self):
        return self.nickname or self.user.username  # Возвращает nickname, если он есть, иначе username
