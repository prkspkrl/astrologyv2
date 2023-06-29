from django.db import models
from django.contrib.auth import get_user_model

from apps.core.models import BaseModel

User = get_user_model()


class Translator(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
