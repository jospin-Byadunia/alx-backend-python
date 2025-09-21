from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

# ----------------------------
# Conversation ViewSet
# ----------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles listing conversations and creating new conversations.
    """
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Expecting participants list (user ids)
        participants_ids = request.data.get('participants', [])
        if not participants_ids or len(participants_ids) < 2:
            return Response(
                {"error": "A conversation must have at least 2 participants."},
                status=status.HTTP_400_BAD_REQUEST
            )
        participants = User.objects.filter(id__in=participants_ids)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ----------------------------
# Message ViewSet
# ----------------------------
class MessageViewSet(viewsets.ModelViewSet):
    """
    Handles listing messages and sending new messages in a conversation.
    """
    queryset = Message.objects.all().select_related('sender', 'conversation')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        sender = request.user
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response(
                {"error": "conversation and message_body are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
