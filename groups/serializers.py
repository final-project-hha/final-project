"""
Serializer for the group API.
"""
from rest_framework import serializers

from groups.models import Group, Admin


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
        admin.groups.set([group.pk])
        group.admins.set([admin.user.pk])

    def create(self, validated_data):
        """Create group and turn creator to admin"""
        user = self.context['request'].user
        group = Group.objects.create(user=user,
                                     created_by=user.email,
                                     **validated_data)

        self._set_creator_of_group_as_admin(user, group)
        return group
