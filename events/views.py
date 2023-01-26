"""
Views for the Event API.
"""
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from events.models import Event
from events.serializers import EventSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from groups.models import Group, Admin

from eventeger.utils import is_member_or_admin, is_admin_or_event_creator


class EventAPIViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """View for the management of events."""
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get', 'patch'])
    def event_details(self, request, group_pk=None, pk=None):
        """Retrieve and manage event by id."""
        event = get_object_or_404(Event, pk=pk)
        if not is_member_or_admin(request.user, event.group):
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            return Response(EventSerializer(event).data)
        if request.method == 'PATCH':
            for attr, value in request.data.items():
                setattr(event, attr, value)
            event.save()
            return Response(data=EventSerializer(event).data, status=status.HTTP_200_OK)


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
        if is_member_or_admin(request.user, group):
            event = Event.objects.create(
                group=group,
                name=request.data['name'],
                description=request.data['description'],
                start_time=request.data['start_time'],
                end_time=request.data['end_time'],
                created_by=request.user,
                location=request.data['location']
            )
            return Response(
                data=EventSerializer(event).data,
                status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

