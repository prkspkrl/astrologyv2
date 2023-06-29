from django.db import models
from django.contrib.auth import get_user_model

from apps.astrologer.models import Astrologer

from apps.core.models import BaseModel
from apps.customer.models import Customer
from apps.translator.models import Translator

User = get_user_model()


class Conversation(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    astrologer = models.ForeignKey(
        Astrologer, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)


class Message(BaseModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    translated_content = models.TextField(null=True, blank=True)
    translator = models.ForeignKey(Translator, on_delete=models.SET_NULL, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Message by {self.sender.username}"
