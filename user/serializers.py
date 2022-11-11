from rest_framework.serializers import ModelSerializer

from user.models import Member, Profile


class MemberSerializer(ModelSerializer):
    class Meta:
        model = Member
        exclude = ['django_user']


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'




