"""
Views for the API.
"""
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from groups.serializers import GroupSerializer
from groups.models import Group, Admin


class GroupViewSet(viewsets.ModelViewSet):
    """View for manage creation of groups API."""
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """Manage deletion of the groups by the admins in a group."""
        user = request.user
        group = self.get_object()

        try:
            admin = Admin.objects.get(user=user)
            if group.admins.contains(admin):
                self.perform_destroy(group)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        except Admin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        """Manage updating of the groups by admins in a group."""
        user = request.user
        group = self.get_object()
        try:
            admin = Admin.objects.get(user=user)
            if group.admins.contains(admin):
                super().update(request)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        except Admin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class MembersAPIView(APIView):
    """Add members to group view"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, group_id, user_id):
        """View for adding a member to a group"""
        group = Group.objects.get(id=group_id)
        user = get_user_model().objects.get(id=user_id)
        try:
            group.admins.get(user__id=request.user.id)
        except Admin.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        group.members.add(user)
        group.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request, group_id):
        """View for listing all members of a group"""
        group = Group.objects.get(id=group_id)
        members = group.members.all()
        admins = group.admins.all()
        group_members = [admins, members]
        return Response(group_members)


