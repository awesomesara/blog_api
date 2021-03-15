from django.db import models

from account.models import User


class Chat(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat')

    def __str__(self):
        return self.comment
