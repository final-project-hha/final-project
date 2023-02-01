"""
Views for the API.
"""
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import users
from groups.serializers import GroupSerializer, ImageSerializer
from groups.models import Group, Admin, Image
from events.models import Event
from events.serializers import EventSerializer

from eventeger.utils import is_user


class GroupViewSet(viewsets.ModelViewSet):
    """View for management of groups API."""
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

    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        """Listing group events, only for members and admins of the group."""
        group = get_object_or_404(Group, pk=pk)
        if request.user in group.members.all():
            events = Event.objects.all()
            return Response([EventSerializer(event).data for event in events])
        try:
            Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            events = Event.objects.all()
            return Response([EventSerializer(event).data for event in events])


class AddMembersAPIView(APIView):
    """Add members to group view"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, group_id, user_id):
        """View for adding a member to a group"""
        group = Group.objects.get(id=group_id)
        if not is_user(user_id):
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            user = get_user_model().objects.get(id=user_id)
        try:
            group.admins.get(user__id=request.user.id)
        except Admin.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        group.members.add(user)
        group.save()
        return Response(status=status.HTTP_200_OK)


class ListMembersAPIView(APIView):
    """View for listing all members and admins
    related to a specific group"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, group_id):
        """
        View for listing all members of a group
        * All app users can view
        """

        group = Group.objects.get(id=group_id)
        members = group.members.values('id', 'name', 'email')
        admins = group.admins.all().values()
        if members:
            return Response({
                "members": members,
                "admins": admins},
                status=status.HTTP_200_OK)
        else:
            return Response({"admins": admins}, status=status.HTTP_200_OK)


class MemberDetailsAPIView(APIView):
    """
    View for deletion and update of members of a group
    * Only admin of the group can delete members and make them admins
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, group_id, user_id):
        """Admin can remove member from the group"""
        group = Group.objects.get(id=group_id)
        try:
            admin = group.admins.get(user=request.user)
            member = group.members.get(id=user_id)
        except Admin.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except users.models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if admin in group.admins.all():
            with transaction.atomic():
                group.members.remove(member)
                group.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, group_id, user_id):
        """Making a member and admin removing from the members list"""
        group = Group.objects.get(id=group_id)
        user = get_user_model().objects.get(id=user_id)

        try:
            group.admins.get(user_id=request.user.id)
        except Admin.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        is_admin = group.admins.filter(user_id=user_id).exists()
        if is_admin:
            with transaction.atomic():
                admin = group.admins.get(user_id=user_id)
                group.members.add(user)
                group.admins.remove(admin)
                Admin.objects.filter(user=user).delete()

        else:
            with transaction.atomic():
                admin = Admin.objects.create(user=user)
                group.members.remove(user)
                group.admins.add(admin)

        return Response(status=status.HTTP_200_OK)


class ImageAPIView(APIView):
    """Manage Images."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, group_id):
        """Upload an image"""
        group = Group.objects.get(id=group_id)
        if not request.data['description']:
            image = Image.objects.create(
                name=request.data['name'],
                image=request.data['image'],
                group=group,
                created_by=request.user
            )
            return Response(
                data=ImageSerializer(image).data,
                status=status.HTTP_201_CREATED)
        if request.data['description']:
            image = Image.objects.create(
                name=request.data['name'],
                image=request.data['image'],
                group=group,
                description=request.data['description'],
                created_by=request.user
            )
            return Response(
                data=ImageSerializer(image).data,
                status=status.HTTP_201_CREATED)

    def get(self, request, group_id, image_id):
        """Get images by id."""
        image = Image.objects.get(id=image_id)
        if group_id == image.group.id:
            return Response(
                data=ImageSerializer(image).data, status=status.HTTP_200_OK)
