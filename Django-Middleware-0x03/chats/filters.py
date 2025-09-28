from django_filters import rest_framework as filters
from .models import Message


class MessageFilter(filters.FilterSet):
    """
    Filter for messages based on sender and date range.
    """
    sender = filters.NumberFilter(field_name="sender__id")
    start_date = filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']