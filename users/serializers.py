"""
Serializers for the User API
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User objects"""
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
