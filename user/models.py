from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

from wallet import models
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user/profile/image", null=True, blank=True, validators=[FileExtensionValidator(["jpg", "jpeg", "png"])])
    address = models.TextField(null=True, blank=True)
    nin = models.CharField(max_length=11, unique=True)
    bvn = models.CharField(max_length=11, unique=True)

