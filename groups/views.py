"""
Views for the API.
"""
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from groups.serializers import GroupSerializer
from groups.models import Group


class GroupViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """View for manage creation of groups API."""
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def destroy(self, request, *args, **kwargs):
    #     """Manage deletion of the groups by the admins in a group."""
    #     user_id = request.user.id
    #     group = self.get_object()
    #     if group.admins.get(id=user_id):
    #         self.perform_destroy(group)
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     else:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
