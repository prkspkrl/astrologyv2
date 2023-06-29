from django.urls import path

from rest_framework.routers import DefaultRouter

from apps.conversation.api.v1.views import (
    ConversationReadOnlyViewSet,
    MessageReadOnlyViewSet,
    InitiateConversationAPIView,
)


router = DefaultRouter()

router.register(r"", ConversationReadOnlyViewSet, basename="conversations")
router.register(
    r"(?P<conversation_id>\d+)/messages", MessageReadOnlyViewSet, basename="messages"
)

urlpatterns = [path("initiate", InitiateConversationAPIView.as_view())] + router.urls
