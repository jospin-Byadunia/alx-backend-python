# chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message

# ----------------------------
# User Serializer
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # for creating/updating users

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'password',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # hash password
        user.save()
        return user


# ----------------------------
# Message Serializer
# ----------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()  # computed field

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',         # nested relation
            'sender_name',    # computed
            'message_body',
            'sent_at',
        ]
        read_only_fields = ['id', 'sent_at', 'sender_name']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"


# ----------------------------
# Conversation Serializer
# ----------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'participants',
            'messages',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        if not self.instance and len(self.initial_data.get('participants', [])) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least 2 participants."
            )
        return attrs
