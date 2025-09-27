from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users to access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Allow only participants to access or modify messages/conversations.
        Explicitly checks HTTP methods for safety.
        """
        user = request.user

        # Safe methods: GET, HEAD, OPTIONS → allow only if participant
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'participants'):
                # obj is a Conversation
                return user in obj.participants.all()
            elif hasattr(obj, 'conversation'):
                # obj is a Message
                return user in obj.conversation.participants.all()
            return False

        # Write methods: POST, PUT, PATCH, DELETE → allow only participants
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()
            elif hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()
            return False

        return False
class IsMessageOwner(permissions.BasePermission):
    """
    Only allow access if the user is the sender of the message.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user