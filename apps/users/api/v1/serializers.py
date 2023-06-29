from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext as _
from django.db import transaction

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    PasswordField,
)

from apps.core.serializers import DummySerializer, DynamicFieldsModelSerializer
from apps.core.validators import validate_attachment

from apps.customer.models import Customer
from apps.astrologer.models import Astrologer

User = get_user_model()


class PasswordChangeSerializer(DummySerializer):
    password1 = PasswordField(max_length=20, min_length=5)
    password2 = PasswordField(max_length=20, min_length=5)

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        if password1 != password2:
            raise serializers.ValidationError(_("Both Password must be same"))
        return super().validate(attrs)


class UserDetailSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        read_only_fields = ("created_at", "last_login", "id")
        fields = (
            "id",
            "full_name",
            "email",
            "gender",
            "phone_number",
            "created_at",
            "is_staff",
            "last_login",
            "profile_picture",
            "role",
        )
        extra_kwargs = {
            "full_name": {"required": True, "allow_blank": False},
            "gender": {"required": False, "allow_blank": True},
            "profile_picture": {
                "required": False,
                "allow_null": True,
                "validators": [
                    FileExtensionValidator(allowed_extensions=["jpg", "png"]),
                    validate_attachment,
                ],
                "use_url": True,
            },
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        lookup="iexact",
                        message=_("You cannot create account with this email address."),
                    )
                ]
            },
            "phone_number": {"validators": []},
        }

    def get_fields(self):
        fields = super().get_fields()
        if self.request and self.request.method.upper() == "POST":
            fields["password1"] = PasswordField(max_length=20, min_length=5)
            fields["password2"] = PasswordField(max_length=20, min_length=5)

        return fields

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(_("Both Password must be same"))
        phone_number = attrs.get("phone_number")

        user_qs = User.objects.all()

        if self.instance:
            user_qs = user_qs.exclude(id=self.instance.id)

        if user_qs.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                {"phone_number": _("You cannot create user with this phone number.")}
            )

        attrs.pop("password2")
        attrs["password"] = attrs.pop("password1")
        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        role = validated_data["role"]
        if role == User.CUSTOMER:
            Customer.objects.create(user=user)
        elif role == User.ASTROLOGER:
            Astrologer.objects.crete(user=user)
        return user


class CustomTokenObtainPairSerializer(DummySerializer, TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserDetailSerializer(instance=self.user).data
        return data
