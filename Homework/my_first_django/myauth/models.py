from django.contrib.auth.models import User
from django.db import models


def avatar_user_directory_path(instance: "Profile", filename: str):
    return f"users/user_{instance.user.pk}/avatar/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_user_directory_path)