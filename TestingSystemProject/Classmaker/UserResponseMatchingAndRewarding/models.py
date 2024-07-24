from django.db import models
from UserResponse.models import UserRegisterModel

class UserResponseScore(models.Model):
    user = models.OneToOneField(UserRegisterModel, on_delete=models.CASCADE, related_name='user_score')
    score = models.PositiveIntegerField()
    ranks = models.PositiveIntegerField()
    persentage = models.FloatField()
    is_passed = models.BooleanField()
    def __str__(self):
        return f'{self.persentage}%'