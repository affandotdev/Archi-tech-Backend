from django.urls import path
from .views import (
    ConversationCreateView,
    ConversationListView,
    MessageCreateView,
    MessageListView,
)

urlpatterns = [
    path("conversations/", ConversationCreateView.as_view(), name="conversation-create"),
    path("conversations/list/", ConversationListView.as_view()),
    path("messages/", MessageCreateView.as_view()),
    path("messages/<uuid:conversation_id>/", MessageListView.as_view()),
]
