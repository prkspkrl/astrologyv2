from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.core.viewsets import CreateListViewSet, ReadOnlyViewSet

from apps.conversation.api.v1.serializers import (
    ConversationSerializer,
    InitiateConversationSerializer,
    MessageSerializer,
)
from apps.conversation.models import Conversation, Message


class InitiateConversationAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = InitiateConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation = Conversation.objects.create(customer=user.customer)
        Message.objects.create(
            conversation=conversation,
            content=serializer.validated_data["content"],
            sender=request.user,
        )
        return Response(data={"id": conversation.id}, status=status.HTTP_201_CREATED)


class ConversationReadOnlyViewSet(ReadOnlyViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(customer__user=self.request.user)
                | Q(astrologer__user=self.request.user)
            )
        )


class MessageReadOnlyViewSet(CreateListViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @property
    def conversation(self):
        conversation_id = self.kwargs["conversation_id"]
        return get_object_or_404(
            Conversation.objects.filter(
                Q(customer__user=self.request.user)
                | Q(astrologer__user=self.request.user)
            ),
            pk=conversation_id,
        )

    def get_queryset(self):
        return super().get_queryset().filter(conversation=self.conversation)

    def perform_create(self, serializer):
        serializer.save(conversation=self.conversation, sender=self.request.user)
