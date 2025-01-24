from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True, null=True)  # Поле для никнейма
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Поле для аватара

    def __str__(self):
        return self.nickname or self.user.username  # Возвращает nickname, если он есть, иначе username

class Idea(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ideas")

    def __str__(self):
        return self.title


class IdeaVote(models.Model):
    VOTE_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)





