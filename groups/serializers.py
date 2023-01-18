"""
Serializer for the group API.
"""
from rest_framework import serializers, status

from groups.models import Group, Admin
from rest_framework.response import Response


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for the groups."""
    class Meta:
        model = Group
        fields = [
            'id', 'group_name', 'created_by', 'created_on',
            'description', 'admins',
        ]
        read_only_fields = [
            'id', 'created_by', 'created_on', 'admins',
        ]

    def _set_creator_of_group_as_admin(self, user, group):
        admin = Admin.objects.create(user=user)
        group.admins.add(admin)

    def create(self, validated_data):
        """Create group and turn creator to admin"""
        user = self.context['request'].user
        group = Group.objects.create(user=user,
                                     created_by=user.email,
                                     **validated_data)

        self._set_creator_of_group_as_admin(user, group)
        return group

    def update(self, instance, validated_data):
        """Update group is only allowed by admins."""
        user = self.context['request'].user
        try:
            admin = Admin.objects.get(user=user)
            if instance.admins.contains(admin):
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)

                instance.save()
                return instance
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Admin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



