import uuid

from django.contrib.auth.models import AbstractUser

from django.db import models

from chat.validators import nickname_validator


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Псевдонім',
        max_length=50,
        unique=True,
        validators=[nickname_validator],
    )
    # nickname = models.CharField(verbose_name='Псевдонім', max_length=50, unique=True, validators=[nickname_validator])
    avatar = models.ImageField(verbose_name='Фото профілю', upload_to='images/avatars/', blank=True, default='images/avatars/default_avatar.png')
    friends = models.ManyToManyField('self')

    # USERNAME_FIELD = "nickname"


class Conversation(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_from_me"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_to_me"
    )
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.from_user.username} to {self.to_user.username}: {self.content} [{self.timestamp}]"
