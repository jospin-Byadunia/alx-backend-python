from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(self.get_serializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing messages and sending a message to a conversation.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a new message to an existing conversation.
        Expects: {
            "conversation": conversation_id,
            "sender": user_id,
            "message_body": "Hello"
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(self.get_serializer(message).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Optionally filter messages by conversation_id via query params.
        """
        queryset = super().get_queryset()
        conversation_id = self.request.query_params.get("conversation_id")
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset
