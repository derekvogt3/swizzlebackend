from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    id = models.CharField(
        primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    