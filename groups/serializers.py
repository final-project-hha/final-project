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
            'id', 'group_name', 'created_by', 'created_on', 'description', 'admins',
        ]
        read_only_fields = [
            'id', 'created_by', 'created_on', 'admins',
        ]

    def create(self, validated_data):
        """Create group."""
        user = self.context['request'].user
        group = Group.objects.create(user=user,
                                     created_by=user.email,
                                     **validated_data)

        admin = Admin.objects.create(user=user)
        admin.groups.set([group.pk])
        group.admins.set([admin.user.pk])
        return group

