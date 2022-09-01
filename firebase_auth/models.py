from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from swizzlebackend.storage_backends import PrivateMediaStorage


class MyUser(AbstractUser):
    id = models.CharField(
        primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    avatar = models.FileField(
        upload_to='avatars', blank=True)
