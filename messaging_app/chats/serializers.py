# chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message

# ----------------------------
# User Serializer
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',          # UUID primary key
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


# ----------------------------
# Message Serializer
# ----------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',          # UUID primary key
            'sender',      # nested user
            'message_body',
            'sent_at',
        ]
        read_only_fields = ['id', 'sent_at']


# ----------------------------
# Conversation Serializer
# ----------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id',             # UUID primary key
            'participants',   # nested users
            'messages',       # nested messages
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
