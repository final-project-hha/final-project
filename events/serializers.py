"""
Serializers for the event model.
"""
from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the Event model."""
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'group']
