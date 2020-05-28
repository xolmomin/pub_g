from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models

UserModel = get_user_model()


class PUser(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    pubg_id = models.CharField(max_length=200, unique=True, null=True, blank=True)
    telegram_id = models.IntegerField(unique=True, null=True, blank=True)
    balance = models.IntegerField(default=0)
    email_verified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    start_time = models.DateTimeField()
    p_user = models.ManyToManyField(PUser, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
