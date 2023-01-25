"""
Views for the Event API.
"""
from datetime import datetime

from rest_framework import mixins, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from events.models import Event
from events.serializers import EventSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from groups.models import Group, Admin


class EventAPIViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """View for the management of events."""
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class EventAPIView(APIView):
    """
    View for creating an event associated inside a group
    Only members nd admins of a group can create events.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, group_id):
        """Create an event with an associated group_id."""
        group = Group.objects.get(id=group_id)
        if request.user in group.members.all():
            event = Event.objects.create(
                group=group,
                name=request.data['name'],
                description=request.data['description'],
                start_time=request.data['start_time'],
                end_time=request.data['end_time'],
                created_by=request.user,
                location=request.data['location']
            )
            return Response(data=EventSerializer(event).data, status=status.HTTP_201_CREATED)
        else:
            flag = group.admins.filter(user=request.user).exists()

            if flag:
                event = Event.objects.create(
                    group=group,
                    name=request.data['name'],
                    description=request.data['description'],
                    start_time=request.data['start_time'],
                    end_time=request.data['end_time'],
                    created_by=request.user,
                    location=request.data['location']
                )
                return Response(data=EventSerializer(event).data, status=status.HTTP_201_CREATED)