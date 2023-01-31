"""
Common function we are using in our main code
such as in the views, tests, and serializers.
"""
from django.contrib.auth import get_user_model
from groups.models import Admin


def is_admin_of_a_group(user, group) -> bool:
    """
    Check if the user is an admin of a group return True
    """
    try:
        group.admins.get(user=user)
    except Admin.DoesNotExist:
        return False
    return True


def is_member_or_admin(user, group) -> bool:
    """
    Check if the user is a member or admin of the group return True.
    """
    if user in group.members.all():
        return True
    try:
        group.admins.get(user=user)
    except Admin.DoesNotExist:
        return False
    else:
        return True


def is_admin_or_event_creator(user, group, event) -> bool:
    """
    Check if the user is a member or admin of the group return True
    """
    if user == event.created_by:
        return True
    try:
        group.admins.get(user=user)
    except Admin.DoesNotExist:
        return False
    else:
        return True


def is_user(user_id):
    """
    Check id there is a user in the database.
    """
    try:
        get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return False
    return True
