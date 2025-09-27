from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsParticipant(permissions.BasePermission):
    """
    Only allow access if the user is a participant in the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()
class IsMessageOwner(permissions.BasePermission):
    """
    Only allow access if the user is the sender of the message.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user