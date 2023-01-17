"""
Views for the API.
"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from groups.serializers import GroupSerializer
from groups.models import Group


class GroupViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """View for manage creation of groups API."""
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
