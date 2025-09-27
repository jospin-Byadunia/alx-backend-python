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
        Check if the user is a participant in the conversation.
        Assumes obj has a 'conversation' field with 'participants' ManyToMany to User,
        or obj itself is a Conversation instance.
        """
        if hasattr(obj, 'participants'):
            # obj is a Conversation
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # obj is a Message
            return request.user in obj.conversation.participants.all()
        return False

class IsMessageOwner(permissions.BasePermission):
    """
    Only allow access if the user is the sender of the message.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user