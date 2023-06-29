from rest_framework import serializers

from apps.customer.models import Customer


class CustomerCreateSSerializer(serializers.ModelSerializer):
    user = UserSer

    class Meta:
        model = Customer
        fields = "__all__"
