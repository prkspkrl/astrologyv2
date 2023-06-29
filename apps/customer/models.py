from django.db import models
from django.contrib.auth import get_user_model

from ..core.models import BaseModel


User = get_user_model()


class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    address = models.CharField(max_length=250, null=True)
    country = models.CharField(max_length=15, null=True)
    state = models.CharField(max_length=15, null=True)
    city = models.CharField(max_length=15, null=True)
    pin_code = models.CharField(max_length=6, null=True)

    def full_address(self):
        return f"{self.address_line_1}, {self.address_line_2}"

    def __str__(self):
        return self.user.email
