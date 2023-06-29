from django.db import models
from django.contrib.auth import get_user_model

from apps.core.models import BaseModel

User = get_user_model()


class Astrologer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year_of_experience = models.PositiveSmallIntegerField(null=True)
