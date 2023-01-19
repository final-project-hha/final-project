"""
Serializer for the group API.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from groups.models import Group, Admin
from users.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for the groups."""
    members = UserSerializer(many=True, required=False)

    class Meta:
        model = Group
        fields = [
            'id', 'group_name', 'created_by', 'created_on',
            'description', 'admins', 'members'
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

    # def update(self, instance, validated_data):
    #     """Update group with new members"""
    #     members = validated_data.pop('members', None)
    #     if members is not None:
    #         instance.members.clear()
    #         for member in members:
    #             member_obj = get_user_model().objects.get(email=member)
    #             instance.members.add(member_obj)
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

