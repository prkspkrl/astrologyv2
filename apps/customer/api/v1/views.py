from rest_framework.viewsets import ModelViewSet

from apps.customer.models import Customer


class CustomerModelViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = Customer
