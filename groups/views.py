"""
Views for the API.
"""
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from groups.serializers import GroupSerializer
from groups.models import Group, Admin
from rest_framework.response import Response


class GroupViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """View for manage creation of groups API."""
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class GroupDetailsViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """View for manage the details of a group in the API"""
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

