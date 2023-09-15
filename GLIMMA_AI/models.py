from django.contrib.auth.models import User
from django.db import models

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # <-- this line creates a link to the User model
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.answer
